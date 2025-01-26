---
layout: post
title:  "Precedence Level ordering with Resets using window functions in SQL"
date:   2025-01-26 12:00:00
author: Ryan Guill
categories: postgresql sql window-functions
tags:	postgresql sql window-functions
---

# Motivation

One of my larger projects at Vendr in the last couple years has been a document extraction system. It uses LLM and other technologies to extract structured data from contracts and other documents, allowing us to build a sizable dataset of all of the actual pricing and negotiation for SaaS software for thousands of companies.

But as we develop our extractions to get new details, or to improve the accuracy of the information, we may extract a document multiple times. We also have human review, correction, and people adding more information from context that may not be in the document. We may be extracting dozens of fields across the extractions, and so we needed a way to determine the precedence of different extractions on a per field per document level.

# The problem at hand: Precedence Level

There is more that goes into how to choose which extraction is the best for an individual document than what I am going to go into here, the whole process is actually quite involved, but I wanted to talk about a particular challenge to allow us to set a precedence level on each extraction (or change it after the fact), to help guide that process.

To start with, we needed two precedence levels - `DEFAULT` and `IMPORTANT`. We would typically set an LLM extraction as `DEFAULT`, and human involved extractions as `IMPORTANT`. An `IMPORTANT` extraction beats a `DEFAULT` one, even if the `DEFAULT` comes after an `IMPORTANT`, but within the same precedence level the last one wins.

But then sometimes we may have an advancement in the LLM extractions that would lead us to want to let it take precedence over any previous extractions, even human guided `IMPORTANT` ones - but from then we would want any future extraction to take precedence again, either a new more recent `DEFAULT` or a new human corrected `IMPORTANT` extraction.

So I wanted to support another precedence level called `RESET`. An extraction with `RESET` should beat anything that came before it, but be treated like `DEFAULT` after that point, with a new `DEFAULT` or `IMPORTANT` taking precedence.

We store all extractions in the database and never get rid of them - we want to keep track of every value that was ever extracted for a field in a document and retain that history, and also we want to be able to adjust the precedence (and other attributes that affect which extraction is the best) at a later date.

To calculate the best extraction I use a SQL function in postgres - so I needed a way to implement this precedence logic using nothing but SQL.

# The SQL challenge

Ordering information by precedence level with just a priority (`IMPORTANT` > `DEFAULT`) is easy in SQL - you just have to assign a sort value to those levels using a join against those values or a case statement plus a timestamp. But implementing something like `RESET` means that a normal sort wont work - the ordering is dependent on a timestamp and if a `RESET` comes before it.

So to do this, you need window functions - in this case `LEAD` or `LAG` - to look at the records before the current row and figure out if there was a `RESET` preceding it. But not just for the record immediately before it, all of them.

Here is an example of the query (much simplified and reworked to try and focus on just the precedence level for clarity):

```sql
with data (id, document_id, value, precedence_level, updated_at) as (
	values
		( 1, 1, 'Z', 'DEFAULT', '2025-01-01'::date)
		, ( 2, 1, 'Y', 'DEFAULT', '2025-01-02') -- later DEFAULT beats previous DEFAULT
		, ( 3, 1, 'X', 'DEFAULT', '2025-01-03') -- later DEFAULT beats previous DEFAULT
		, ( 4, 1, 'E', 'IMPORTANT', '2025-01-04') -- IMPORTANT beats DEFAULT
		, ( 5, 1, 'F', 'DEFAULT', '2025-01-05') -- previous IMPORTANT beats this record
		, ( 6, 1, 'D', 'IMPORTANT', '2025-01-06') -- later IMPORTANT beats previous IMPORTANT
		, ( 7, 1, 'C', 'RESET', '2025-01-07') -- RESET beats everything else
		, ( 8, 1, 'B', 'DEFAULT', '2025-01-08') -- bc last record was RESET this DEFAULT now takes precedence
		, ( 9, 1, 'A', 'IMPORTANT', '2025-01-09') -- IMPORTANT overrides DEFAULT
)
, data_with_resets as (
	select *
		, count(*)
			filter (where data.precedence_level = 'RESET')
			over (
				partition by document_id
				order by updated_at asc
			) prev_reset_count
	from data
)
, calculate_ranking as (
	select
		dense_rank() over (
			partition by document_id
			order by
				(prev_reset_count * 10) +
				(data.precedence_level = 'IMPORTANT')::int * 5
					desc
				, updated_at desc
		) as rnk
		, *
	from data_with_resets data
	order by 1
)
, data_with_prev_value as (
	select *
		, lead(value) over (partition by document_id order by rnk) prev_value
	from calculate_ranking
)
, final as (
	select
		dense_rank() over (ORDER BY rnk, updated_at desc ) rnk_final
		, *
	from data_with_prev_value
	order by 1 asc
)
select *
from final
;
```

You can play with this query and the parts of it here: https://dbfiddle.uk/HBKDOaR3?highlight=16

The key parts that make this work start with the `data_with_resets` CTE. Here we count how many preceding rows are a `RESET` precedence level using a window for the same document ordered by the timestamp. It isn't necessarily obvious from this code unless you are familiar with window functions, but when you use count with a window (the `over` clause) it is a running count up to and including the current row.

Then the actual logic happens in the `calculate_ranking` CTE. we use a `dense_rank` which gives us a consecutive ranking without gaps. We partition by the document and then we order by the precedence level. We add 10 for each `RESET`, `DEFAULT` is treated as 0 and `IMPORTANT` is treated as 5, then ordering by the timestamp.

The next CTE isn't required for our purpose here, but allows us to figure out what the previous value was, based on the same precedence ordering, so we can tell if something changed.

Technically the last `final` CTE isn't strictly necessary, but it allows us to get a single ranking field to order the final recordset by.

# Conclusion

The main takeaway I hope to convey with this post is that SQL traditionally has you think in terms of sets of data which is very powerful, but sometimes you need to be able to work iteratively and consider the previous or next row, or a window of rows not including the entire set. Window functions extend your capabilities of what you can achieve in a single SQL query and using only your database, keeping you from having to do this work in the application layer, increasing performance and lowering your memory and network utilization.


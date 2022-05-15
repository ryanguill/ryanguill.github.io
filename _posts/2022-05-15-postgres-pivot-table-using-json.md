---
layout: post
title:  "Postgres pivot table using JSON"
date:   2022-05-15 12:00:00
author: Ryan Guill
categories: postgresql sql
tags:	postgresql sql
---

Something I have a need to do often but can be difficult to do at times in SQL is to create a pivot table. As an example imagine wanting to see customers and their revenue by month. It is straightforward to create a normal data set where the dates are the rows and you have a revenue amount for each. Something like this: 

|        dte | total |
|-----------:|------:|
| 2022-01-01 | 22030 |
 | 2022-02-01 | 22753 |
 | 2022-03-01 |     0 |
 | 2022-04-01 |  9456 |
 | 2022-05-01 |  7798 |
 | 2022-06-01 | 38278 |
 | 2022-07-01 | 18736 |
 | 2022-08-01 |  6794 |
 | 2022-09-01 | 21033 |
 | 2022-10-01 | 28576 |
 | 2022-11-01 | 10172 |
 | 2022-12-01 | 41901 |

But you quickly come up to two obstacles as you try to take it further - you either want to have the months as columns like this:


|   jan |   feb | mar |  apr |  may |   jun |   jul |  aug |   sep |   oct |   nov |   dec |
|------:|------:|----:|-----:|-----:|------:|------:|-----:|------:|------:|------:|------:|
| 22030 | 22753 |   0 | 9456 | 7798 | 38278 | 18736 | 6794 | 21033 | 28576 | 10172 | 41901 |


or you want to see multiple customers, which as a column can be difficult, or even harder is having the months as columns and the customers as rows:

|      cus_id |   jan |   feb | mar |  apr |  may |   jun |   jul |  aug |   sep |   oct |  nov |   dec |  
|------------:|------:|------:|----:|-----:|-----:|------:|------:|-----:|------:|------:|-----:|------:|
|           1 |     0 | 10170 |   0 | 5399 |    0 | 14821 |  7927 |    0 |    14 | 15466 | 3675 | 14447 |
|           2 | 22030 | 12583 |   0 | 4057 | 7798 | 23457 | 10809 | 6794 | 21019 | 13110 | 6497 | 27454 |

The term for this is pivot table - which is something you may have done many times in Excel or other spreadsheet application.

But this is difficult in SQL, because SQL requires you to have a static column list. You can't ask SQL to give you whatever columns are necessary, you must declare them in your query. (`SELECT *` may seem like an exception to this rule, but in this case the SQL engine still knows what the columns are going to be before the query is executed).

Luckily Postgres gives you a way around this. If you want actual columns you still have to specify them, but the hard part of aggregation into these pivoted columns and rows are made much easier. The key is using the JSON functionality, which allows you to represent complex values in a single cell. It allows you to aggregate the values into what really represents multiple values, and then pull them back apart after the fact.

Here is an example of what this looks like:

```sql
WITH columns AS (
  SELECT
       generate_series dte
     , customer_id
  FROM generate_series('2022-01-01'::date, '2022-12-31', '1 month')
  CROSS JOIN
    (
      SELECT DISTINCT
        customer_id
      FROM
        invoice
    ) AS customers
), data AS (
  SELECT
      columns.dte
    , columns.customer_id
    , SUM(COALESCE(invoice.amount, 0)) total
  FROM columns
  LEFT OUTER
    JOIN invoice
    ON DATE_PART('year', invoice_date) = DATE_PART('year', columns.dte)
    AND DATE_PART('month', invoice_date) = DATE_PART('month', columns.dte)
    AND columns.customer_id = invoice.customer_id
  GROUP BY
      columns.dte
    , columns.customer_id
), result AS (
  SELECT
    customer_id
    , JSONB_OBJECT_AGG(TO_CHAR(dte, 'YYYY-MM'), total) pivotData
  FROM
    data
  GROUP BY
    customer_id
)
SELECT
    customer_id
  , (pivotData->>'2022-01') "jan"
  , (pivotData->>'2022-02') "feb"
  , (pivotData->>'2022-03') "mar"
  , (pivotData->>'2022-04') "apr"
  , (pivotData->>'2022-05') "may"
  , (pivotData->>'2022-06') "jun"
  , (pivotData->>'2022-07') "jul"
  , (pivotData->>'2022-08') "aug"
  , (pivotData->>'2022-09') "sep"
  , (pivotData->>'2022-10') "oct"
  , (pivotData->>'2022-11') "nov"
  , (pivotData->>'2022-12') "dec"
FROM
  result
ORDER BY customer_id
```

Which gives results like we were after above.

If you would like to see how this is done, I have an interactive fiddle you can play with that shows you step by step how each of these parts work: 

[https://dbfiddle.uk/?rdbms=postgres_14&fiddle=39e115cb8afd6e62c0101286ecd08a3f](https://dbfiddle.uk/?rdbms=postgres_14&fiddle=39e115cb8afd6e62c0101286ecd08a3f)

This example is using PG 15, but this functionality works all the way back to PG 9.5.

This query is also a great example of using `generate_series` to generate a set of data to join against, so that you can find any holes and represent all the data points you need (months in this case), even if there is no actual data for that point.

In conclusion, the JSON functionality built into todays relational databases are more than just schemaless data stores and complex values in cells. They can also be powerful as intermediate steps to help you manipulate and transform your data in useful ways.

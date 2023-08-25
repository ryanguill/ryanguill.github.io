---
layout: post
title: "Notes on PostgreSQL Explain Analyze"
date: 2023-08-25 12:00:00
author: Ryan Guill
categories: postgresql sql
tags: postgresql sql
---


One thing you'll want to learn if you use PostgreSQL for any length of time is how to use `EXPLAIN`. At my job at Vendr, like my previous roles, we are no exception. The good and bad thing is that in many cases you can go pretty far before you start having issues. But that means that not everyone has had the opportunity to learn the dark art of reading explain output. And as great as PG is, it is not as user friendly in this area as other RDBMs like MSSQL. But with this primer, a few free online tools, and a little bit of time, you can quickly learn how to think about the performance of your queries and where to start when optimizing.

<!-- break -->

The first thing to know is that you almost always want to use `EXPLAIN ANALYZE`, but its important to understand that the `ANALYZE` keyword will cause PG to actually execute your query so it can give you an execution time. This has two consequences:

If you use `EXPLAIN ANALYZE` on DML statements (that is `INSERT`, `UPDATE`, `DELETE`, statements, calling functions which do these things, etc), it will actually _run_ those statements. So you want to make sure you are in a transaction that you can roll back.

And even though `EXPLAIN ANALYZE` runs the statement, it throws away the actual results. 

But returning data to the client can be a significant part of the execution time of any given statement! Here is an example:

```sql
explain analyze verbose
select n
, repeat('abcdefghijklmnopqrstuvwxyz ', 100)
from generate_series(1,2000) as x(n);
```

When I run this the explain returns:

```
+------------------------+
|QUERY PLAN              |
+------------------------+
|Planning Time: 0.038 ms |
|Execution Time: 0.459 ms|
+------------------------+
```

But if I run the query (without the explain) I see:

```
2,000 rows retrieved starting from 1 in 2 s 305 ms
```

Which is a difference of more than 2000x. The network costs completely swamp the complexity of the actual statement.

So two things to draw from this: make sure you understand the difference between how long it takes to plan and execute a statement on the database vs how long it takes to return the data to the client; and this is why you want to be as selective as you can about what you return to the client. This is why `SELECT *` is bad (well, one of many reasons). If you can, only returning the data you actually need (both rows and columns) can make a significant difference to the speed of your queries and thus application.

The next main topic I want to mention is about the `cost` values you see in `EXPLAIN` output. 

`cost` values should be considered unit-less, and should only be used to compare queries doing similar things, and only against the same database instance.  Costs are calculated using many different things, such as the data you have in your database, the statistics it has gathered about that data, the parameters in that instance such as `work_mem`, etc. You cannot compare costs directly from dev environment and production, they can be two completely different things, even if they look comparable.

What you can do is compare a query to a different version of the same query (against the same instance) to see if you are improving things or not and on what scale. You can also compare them inside of a single query plan to understand the highest cost parts of your query.

But don't get hung up on the cost numbers themselves. Use them as a relative measurement, they are not hard and fast numbers.

Also you may need to run your query against the production database to get accurate information like you see in your application. This is a sliding scale - sometimes you can get a good idea just from a development database, sometimes you need a bit more realistic example from a staging or similar server that has a copy of the production data, but sometimes you need to go to production to really see representative data. Another thing to consider is if you use read-replicas and primaries, you may need to go to whichever is going to be the place your query is actually going to be executed against in your application.

As far as what you are looking for when reading `EXPLAIN` output, that is a much larger topic. But the place to start will always be to look for `Seq Scan`. Nine times out of ten that is where you should focus your efforts. The one time out of ten it might actually be faster than an index because the table is small or the indexes aren't very useful, but most of the time you want to be using an index. Ideally you want an `Index Only Scan`. This means that it was able to get all of the data from the index and didn't have to go to the actual table. Next best is an `Index Scan`. 

The next thing most common you are looking for when trying to improve query performance is `Nested Loop`. These will be places where things cant be done in a batch and has to be looped over. The fix here isn't always straight forward, but oftentimes is a matter of doing a better filter earlier in the execution of the query.

This information is of course nowhere near exhaustive, just a place to start. I am far from an expert in understanding query plans, I learn more all the time. If you need more you should look at resources such as https://use-the-index-luke.com/, or use explain visualization tools such as https://explain.dalibo.com/, https://tatiyants.com/pev/#/plans, https://explain.depesz.com/ or https://www.pgexplain.dev/

But like most things the best thing you can do is practice, play with queries and explain output and keep reading to understand what is happening. In my experience you can generally get great performance with a little work in most cases.

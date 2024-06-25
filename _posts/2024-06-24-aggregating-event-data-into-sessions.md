---
layout: post
title:  "Aggregating event data into sessions using SQL"
date:   2024-06-24 12:00:00
author: Ryan Guill
categories: postgresql sql
tags:	postgresql sql
---

Lets say you have a table of events, each representing a point in time when an event occurred. Maybe it's clicks in your applications, or pages that a user visited. You might like to see how long users are spending in your application, or what they are doing in a given session.

So the task at hand is to use SQL to analyze this event data and combine these points in time into groups of events - I will call them sessions for this post.

The first thing you must do is decide how much time you would allow someone to go before another event happens for it to still be considered the same session. Anything less than this duration between events, and the events are connected into the same session; anything more, and we will call it a new session. The value you use here is up to you and your needs - if the actions you are looking at take a lot of time to perform, or maybe someone is spending time reading a lot of content before continuing to the next thing, you might want to make this threshold higher, maybe tens of minutes or even more. On the other hand, if you expect they should be clicking around fairly quickly, you might want to go much shorter, maybe only seconds. For this example I am going to use 5 minutes between events as my threshold.

The next thing you need to decide is, if the session only lasted for one event, how long would you want to say it lasted? For this example, I am going to use 1 minute.

So there are several SQL features we can use to our advantage - this is all PostgreSQL; everything here works at least as far back as version 9.5, possibly earlier.

The first feature is Postgres' interval type. If you haven't played with intervals, you are really missing out. It is a native data type that defines a period of time - perfect for our use cases.

The next thing to understand is window functions. I have been writing SQL long enough that these still feel "new", but they have been around for a long time now! Window functions are great; they let you aggregate against different partitions (groups, or in this case windows) in the same query, which is perfect for our needs where we want to consider each user independently.

Let's look at some example data to get our bearings:

```sql
DROP TABLE IF EXISTS event_log CASCADE;
CREATE TABLE event_log (
	  ts timestamptz
	, name varchar
);

INSERT INTO event_log ( ts, name ) VALUES
  ('2024-07-01T12:00:00.000Z', 'Alice')
, ('2024-07-01T12:01:00.000Z', 'Alice')
, ('2024-07-01T12:02:00.000Z', 'Alice')
, ('2024-07-01T12:03:00.000Z', 'Alice')
, ('2024-07-01T12:04:00.000Z', 'Alice')
, ('2024-07-01T12:05:00.000Z', 'Alice')
, ('2024-07-01T12:12:00.000Z', 'Alice')
, ('2024-07-01T12:14:00.000Z', 'Alice')
, ('2024-07-01T12:17:00.000Z', 'Alice')
, ('2024-07-01T12:21:00.000Z', 'Alice')
, ('2024-07-01T12:26:00.000Z', 'Alice')
, ('2024-07-01T12:30:00.000Z', 'Alice')
, ('2024-07-01T12:00:00.000Z', 'Bob')
, ('2024-07-01T12:02:00.000Z', 'Bob')
, ('2024-07-01T12:05:00.000Z', 'Bob')
, ('2024-07-01T12:09:00.000Z', 'Bob')
, ('2024-07-01T12:14:00.000Z', 'Bob')
, ('2024-07-01T12:20:00.000Z', 'Bob')
, ('2024-07-01T12:25:00.000Z', 'Bob')
, ('2024-07-01T12:35:00.000Z', 'Bob')
, ('2024-07-01T12:44:00.000Z', 'Bob')
, ('2024-07-01T12:48:00.000Z', 'Bob')
, ('2024-07-01T13:05:00.000Z', 'Bob')
;
```

Here you can see we have two users, Alice and Bob, and they have several events. Of course, in a real world scenario, these names would probably be IDs to a users table, you would have an event type and probably lots of other attributes for the event, but none of that is necessary for this demo. If you have trouble extending this example to a more real world scenario, reach out in the comments or on Twitter.

Here is the final query, we will walk through the different parts of it to see how it works:

```sql
with inputs as (
  select
      '5 minutes'::interval threshold -- change this to however long you want your session timeouts to be
    , '1 minute'::interval min_session_duration -- if there is only one event in the session, how long do you want to say it lasted?
)
, prep as (
  select
      ts
    , name
    , row_number() 
      over (partition by name order by ts) row_num
    , coalesce(
      ts - lag(ts) 
        over (partition by name order by ts asc) <= inputs.threshold
      , false) is_connected
  from
    event_log
  cross
    join inputs
)
, session_detail as (
  select
      ts
    , name
    , max(row_num) 
      filter (where NOT is_connected) 
      over (partition by name order by ts asc) session_seq
  from prep
)
, sessions as (
  select
      row_number() 
      over (partition by name order by min(ts), session_seq) session_seq
    , name
    , count(*) event_count
    , min(ts) start_ts
    , max(ts) end_ts
    , greatest(inputs.min_session_duration, max(ts) - min(ts)) session_duration
  from session_detail
  cross
    join inputs
  group by
      session_seq
    , name
    , inputs.min_session_duration
)
select
    session_seq
  , concat_ws('-', name, session_seq) unique_id
  , name
  , event_count
  , start_ts
  , end_ts
  , session_duration
from sessions
;
```

If you arent comfortable with SQL that might look like a lot, but trust me, its really not bad - and we will walk through all the different parts.

Here is what the query returns (I have removed the date and seconds and milliseconds for the timestamps for brevity, they are all the same for the example):

<style>
    table.data-view {
        font-size:smaller;
    }
        table.data-view tbody tr td {
            padding: 5px;
        }

        td.right, th.right {
            text-align: right;
        }

        td.center, th.center {
            text-align: center;
        }
</style>


<table class="data-view"><thead>
  <tr>
    <th class="right">session_seq</th>
    <th>unique_id</th>
    <th>name</th>
    <th class="right">event_count</th>
    <th class="center">start_ts</th>
    <th class="center">end_ts</th>
    <th class="center">session_duration</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="right">1</td>
    <td>Alice-1</td>
    <td>Alice</td>
    <td class="right">6</td>
    <td class="center">12:00</td>
    <td class="center">12:05</td>
    <td class="center">00:05:00</td>
  </tr>
  <tr>
    <td class="right">2</td>
    <td>Alice-2</td>
    <td>Alice</td>
    <td class="right">6</td>
    <td class="center">12:12</td>
    <td class="center">12:30</td>
    <td class="center">00:18:00</td>
  </tr>
  <tr>
    <td class="right">1</td>
    <td>Bob-1</td>
    <td>Bob</td>
    <td class="right">5</td>
    <td class="center">12:00</td>
    <td class="center">12:14</td>
    <td class="center">00:14:00</td>
  </tr>
  <tr>
    <td class="right">2</td>
    <td>Bob-2</td>
    <td>Bob</td>
    <td class="right">2</td>
    <td class="center">12:20</td>
    <td class="center">12:25</td>
    <td class="center">00:05:00</td>
  </tr>
  <tr>
    <td class="right">3</td>
    <td>Bob-3</td>
    <td>Bob</td>
    <td class="right">1</td>
    <td class="center">12:35</td>
    <td class="center">12:35</td>
    <td class="center">00:01:00</td>
  </tr>
  <tr>
    <td class="right">4</td>
    <td>Bob-4</td>
    <td>Bob</td>
    <td class="right">2</td>
    <td class="center">12:44</td>
    <td class="center">12:48</td>
    <td class="center">00:04:00</td>
  </tr>
  <tr>
    <td class="right">5</td>
    <td>Bob-5</td>
    <td>Bob</td>
    <td class="right">1</td>
    <td class="center">13:05</td>
    <td class="center">13:05</td>
    <td class="center">00:01:00</td>
  </tr>
</tbody></table>

Lets start with the two pieces of SQL that make this work.

First theres this line:

```sql
, coalesce(
    ts - 
    lag(ts) over (partition by name order by ts asc) 
        <= inputs.threshold
    , false) is_connected
```

Forgive the formatting - there is no great way to format it that will make everyone happy, but hopefully I can walk you through the pieces.

The goal with this line is to get true or false, is the row we are looking at part of the same session as the previous event for the user.

Starting from the inside out - for the current row, we are taking its ts (timestamp), and subtracting the timestamp of the row before it. This is a window function - you know that because of the `over ()` clause. The window is how we decide what "before it" means. 

We are using `partition by name`, meaning that our window will always only consider rows that have the same values for name as our current row - and we are using `order by ts asc`, meaning "before" will be a row _earlier_ than the current row.  

`partition by` works just like `group by`, you are defining the individual groupings of columns whose combination of values are considered unique to define your different groups. In our case, we only want to consider rows by the same user.

`lag()` is just one option, theres its dual `lead()`, which if you were to order by `desc` instead would work just the same.

We do our subtraction and get an interval - a duration of time since that previous event. Now we just need to know if that interval is less than our threshold - if so we are still part of the same session, if not then this is the beginning of a new session.

But our `lag(ts) ...` could return `null` - if we are looking at the first event for a user, there is no previous value. And so if we take our current row's timestamp and subtract `null`, the result will of course be `null`. And when we do our comparison with the threshold, we will also get `null`. So we `coalesce()` our value to `false` in that case - if it's the first event for a user it certainly cannot be part of a previous session.

So now lets look at the other important part of this approach:

```sql
, max(row_num) 
      filter (where NOT is_connected) 
      over (partition by name order by ts asc) session_seq
```

This part is a little more complicated, so bear with me:

Earlier in the query we assigned a row number to each row with the `row_number()` window function, using the same partitions as we previously discussed. 

Our goal is to get the highest row number that was the beginning of the current session - so we are only interested in rows where `is_connected` is false. 

The most important thing to understand is that `max()` as a window function that includes an `order by` clause will not consider the entire window, but only the window _frame_ up to the current row. I'm going to quote the postgres documentation here: <sup>[1](https://www.postgresql.org/docs/current/tutorial-window.html)</sup>

> There is another important concept associated with window functions: for each row, there is a set of rows within its partition called its window frame. Some window functions act only on the rows of the window frame, rather than of the whole partition. By default, if ORDER BY is supplied then the frame consists of all rows from the start of the partition up through the current row, plus any following rows that are equal to the current row according to the ORDER BY clause. When ORDER BY is omitted the default frame consists of all rows in the partition.

So our `max()` is only considering rows where `is_connected` is false, meaning the events that were the beginning of sessions. Then we want to pick the highest row number that came before the current row - so if we are in the second session we want to pick the beginning of the second session.

These are the two most important parts of this solution - how to figure out if the current row is a continuation of a session or the start of a new one, and then how to find the start of the session for the current row, so we know which session we are a part of.

The one other thing I want to call out here is the CTE at the top I call `inputs` - this is a pattern I use a lot - it pulls the "variables" of a query to the top, and just selects them as literal values - then I can cross join them where I need to in the rest of the query, making it dynamic to those inputs.

Here is a database fiddle if you want to play with this query to understand it better. I really recommend pulling out parts of the CTEs and understanding how each part works: [https://dbfiddle.uk/M_iWoTG-](https://dbfiddle.uk/M_iWoTG-)

One last thing to mention is that this query is useful if you want to slice and dice your event data in a few different ways to explore it. You might get different results and gain more insights into your data if you tweak the thresholds. However, if you already have these thresholds set in stone, this would be an easy thing to calculate as your data comes in, or in an intermediate table, ingesting the event data on some period and calculating the duration from the previous event and which session they were a part of.
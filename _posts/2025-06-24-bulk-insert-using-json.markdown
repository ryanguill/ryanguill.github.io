---
layout: post
title:  "Bulk insert into postgres using a single parameter"
date:   2025-06-24 12:00:00
author: Ryan Guill
categories: postgresql sql json
tags:	postgresql sql json
---

# motivation

At my job recently we had a need to bulk insert lots of records quickly and efficiently, but we had some limitations we needed to work around. We have been using Prisma for a while, which has a `createMany` function to insert multiple rows, but something we have changed or upgraded recently (we aren't sure what exactly) was causing it to actually insert rows one at a time instead. This isn't too big of a deal if you are only inserting a few rows at a time, but we needed to insert hundreds to tens of thousands of rows at a time and doing them one by one wasn't going to cut it.

We have also very recently started using [Prisma's typedSQL](https://www.prisma.io/typedsql) functionality to allow us to write real SQL and still get type safety as well, which is great, except it doesn't handle a variable number of parameters.

So I had the idea to instead send a single parameter into the statement as JSON, an array of objects, then parse that into a recordset, and use that to insert into the database.

# example

Here is what that looks like:

```sql
WITH raw_input(json_blob) AS (
    -- In production you would pass $1 here;
    VALUES (
        $$[
            {
              "id":           "9f2ddc93-0db3-46d2-a2cb-e6df4418faad",
              "key":          "status",
              "value":        "active",
              "created_at":   "2025-06-24T12:34:56Z",
              "updated_at":   "2025-06-24T13:45:00Z"
            },
            {
              "id":           "b8f9152e-a203-4d0a-b530-0a4e45c9b0a9",
              "key":          "priority",
              "value":        "high",
              "created_at":   "2025-06-24T12:34:56Z",
              "updated_at":   "2025-06-24T13:45:00Z"
            }
        ]$$::json
    )
)
-- Expand the JSON array to a proper recordset
, parsed AS (
    SELECT *
    FROM raw_input
    CROSS JOIN LATERAL json_to_recordset(json_blob) AS r(
        id          uuid,
        key         text,
        value       text,
        created_at  timestamptz,
        updated_at  timestamptz
    )
)
-- Bulk-insert the rows in a single SQL statement
INSERT INTO target_table (
      id, key, value, created_at, updated_at
)
SELECT
      id, key, value, created_at, updated_at
FROM   parsed
RETURNING *;
```

You can try it for yourself here: https://dbfiddle.uk/Am4xRgbz

There are only two parts to really understand here:

`json_to_recordset` takes a json blob and a schema for the resulting recordset and parses your data into a recordset. You don't have to reference or use all keys in the json, and if you provide a column that doesn't have a matching key you will get `null` for those values.

The only other thing to know is that you need to use `CROSS JOIN LATERAL`, this will parse each record individually giving you one row per object.

And that's all there is to it. Now we have a statement that takes a single input, but that input can contain thousands of rows. The limit for a single parameter into a statement is an entire gigabyte of data, so you can use this to insert a lot of data at once.

The difference for us was significant. When inserting 1k records individually it was timing out after 60s. Even inserting in batches of 250 at a time using the previous `createMany` functionality it was taking 10's of seconds. This was able to do it in less than a second every time, usually less than a 1/4 of a second.

Of course you could use this with `ON CONFLICT DO UPDATE` for upserts, or just as a way to get data into a statement for joining with other data. And you can enrich the `json_to_recordset` definition with default columns, `CHECK` constraints, or even a `WHERE` clause inside the CTE to filter out data early before you insert. Even join with other data in the database.

# full SQL example

Adding the full SQL example here in case the dbfiddle link ever stops working:

```sql

create table target_table (id uuid, key text, value text, created_at timestamptz, updated_at timestamptz);

WITH raw_input(json_blob) AS (
    -- In production you would pass $1 here;
    VALUES (
        $$[
            {
              "id":           "9f2ddc93-0db3-46d2-a2cb-e6df4418faad",
              "key":          "status",
              "value":        "active",
              "created_at":   "2025-06-24T12:34:56Z",
              "updated_at":   "2025-06-24T13:45:00Z"
            },
            {
              "id":           "b8f9152e-a203-4d0a-b530-0a4e45c9b0a9",
              "key":          "priority",
              "value":        "high",
              "created_at":   "2025-06-24T12:34:56Z",
              "updated_at":   "2025-06-24T13:45:00Z"
            }
        ]$$::json
    )
)
-- Expand the JSON array to a proper recordset
, parsed AS (
    SELECT *
    FROM raw_input
    CROSS JOIN LATERAL json_to_recordset(json_blob) AS r(
        id          uuid,
        key         text,
        value       text,
        created_at  timestamptz,
        updated_at  timestamptz
    )
)
-- Bulk-insert the rows in a single SQL statement
INSERT INTO target_table (
      id, key, value, created_at, updated_at
)
SELECT
      id, key, value, created_at, updated_at
FROM   parsed
RETURNING *;


-- example so you can see what the parsed data looks like
WITH raw_input(json_blob) AS (
    VALUES (
        $$[
            {
              "id":           "9f2ddc93-0db3-46d2-a2cb-e6df4418faad",
              "key":          "status",
              "value":        "active",
              "created_at":   "2025-06-24T12:34:56Z",
              "updated_at":   "2025-06-24T13:45:00Z"
            },
            {
              "id":           "b8f9152e-a203-4d0a-b530-0a4e45c9b0a9",
              "key":          "priority",
              "value":        "high",
              "created_at":   "2025-06-24T12:34:56Z",
              "updated_at":   "2025-06-24T13:45:00Z"
            }
        ]$$::json
    )
)
, parsed AS (
    SELECT *
    FROM raw_input
    CROSS JOIN LATERAL json_to_recordset(json_blob) AS r(
        id          uuid,
        key         text,
        value       text,
        created_at  timestamptz,
        updated_at  timestamptz
    )
)  
select * from parsed;

select * from target_table;

```
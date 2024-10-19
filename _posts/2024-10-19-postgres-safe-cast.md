---
layout: post
title:  "safe_cast function in postgresql"
date:   2024-10-17 12:00:00
author: Ryan Guill
categories: postgresql sql
tags:	postgresql sql
---
I love using JSON in postgres. When support for JSON types and functionality first started coming out in SQL I generally thought it was neat but that it wouldn't be something I would ever want to use in production. I could not have been more wrong.

I could talk at length (and have) about all the ways that it is useful, but if you do you will find that the main way you pull information out of JSON will bring it out as TEXT. And frequently when you're using JSON you can't be sure that the data is exactly the right format you expect anyway. Lately I store a lot of JSON that comes back from LLMs, and while it gets it right most of the time, you can never really be sure - you need to trust be verify.

So I have been using this function for a long time to safely convert from text to a given datatype in SQL. If the cast can be made successfully it will, otherwise it will return the second argument as a default - most of the time I use `null` but it can be anything.

```sql
/* 
  utility function to convert from text to various data types
    , such as when you are pulling values out of json 
  The function will cast the value of the first argument 
    to the type of the second argument.
  If the first argument cannot be convert to the target type
    the value of the second argument will be returned as the default.
  If you want to return null as the default, cast the null to the target
    type like `null::integer` or `null::date`
*/
DROP FUNCTION IF EXISTS safe_cast(text, anyelement);
CREATE OR REPLACE FUNCTION safe_cast(text, anyelement)
RETURNS anyelement
LANGUAGE plpgsql as $$
BEGIN
    $0 := $1;
    RETURN $0;
    EXCEPTION WHEN OTHERS THEN
        RETURN $2;
END;
$$;
```

The function itself looks a little terse and strange, but if you look and play with the examples you'll get a better understanding of how it works. I have been using it for a long time, I can't remember if I actually wrote it or got it from somewhere else - I believe I may have adapted it from this answer on stackoverflow: [https://stackoverflow.com/a/2095676/7186](https://stackoverflow.com/a/2095676/7186)

Below are examples, but you can play with the function and these examples here: [https://dbfiddle.uk/3kAop9-Z](https://dbfiddle.uk/3kAop9-Z)

```sql

select
	  safe_cast('true', false::boolean) = true
	, safe_cast('false'::text, false::boolean) = false
	, safe_cast('yes'::text, false::boolean) = true
	, safe_cast('no'::text, false::boolean) = false
	, safe_cast('on'::text, false::boolean) = true
	, safe_cast('off'::text, false::boolean) = false
	, safe_cast('1'::text, false::boolean) = true
	, safe_cast('0'::text, false::boolean) = false
	, safe_cast(1::text, false::boolean) = true
	, safe_cast(0::text, false::boolean) = false
	, safe_cast('foo'::text, false::boolean) = false
	, safe_cast('3'::text, false::boolean) = false
	, safe_cast(3::text, false::boolean) = false
	, safe_cast('', false::boolean) = false
	, safe_cast(null::text, false::boolean) is null
	;

select
	  safe_cast('123', null::numeric) = 123::numeric
	, safe_cast('123.45', null::numeric) = 123.45::numeric
	, safe_cast('0', null::numeric) = 0::numeric
	, safe_cast('-1', null::numeric) = -1::numeric
	, safe_cast('-1.2', null::numeric) = -1.2::numeric
	, safe_cast('123x', null::numeric) is null
	, safe_cast('', null::numeric) is null
	, safe_cast('foobar', null::numeric) is null
	, safe_cast('123', null::numeric) > 1
    , safe_cast('123', 0::integer) = 123::integer
	, safe_cast('', 0::integer) = 0::integer
	, safe_cast('foo', 0::integer) = 0::integer
	;

select
	  safe_cast('2024-01-02', null::date) = '2024-01-02'::date
	, safe_cast('01-02-2024', null::date) = '2024-01-02'::date
	, safe_cast('2024-01-023', null::date) = '2024-01-23'::date --possibly surprising
	, safe_cast('2024-01-', null::date) is null
	, safe_cast('2024-01-123', null::date) is null
	, safe_cast('2024', null::date) is null
	, safe_cast('foobar', null::date) is null
    , safe_cast('2024-01-02', null::timestamptz) = '2024-01-02 00:00:00'::timestamptz
	;
```

Other databases have similar functionality built in, but most do not have the ability to set a default if it fails baked into the function, most just return null. (The following list is the ones I know off the top of my head, and is not meant to be exhaustive)

MSSQL has `TRY_CAST`: [https://learn.microsoft.com/en-us/sql/t-sql/functions/try-cast-transact-sql?view=sql-server-ver16](https://learn.microsoft.com/en-us/sql/t-sql/functions/try-cast-transact-sql?view=sql-server-ver16)

Snowflake has `TRY_CAST`: [https://docs.snowflake.com/en/sql-reference/functions/try_cast](https://docs.snowflake.com/en/sql-reference/functions/try_cast)

DuckDb has `TRY_CAST` [https://duckdb.org/docs/sql/expressions/cast.html#try_cast](https://duckdb.org/docs/sql/expressions/cast.html#try_cast)


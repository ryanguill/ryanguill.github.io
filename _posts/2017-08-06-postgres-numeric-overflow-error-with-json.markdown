---
layout: post
title:  "Postgres numeric overflow error with json"
date:   2017-08-06 00:00:00
author: Ryan Guill
categories: postgres sql json
tags:	postgres sql json
---

Recently I came across an error using postgres that stumped me for a while so I wanted to document it for next time.  I was issuing an update statement to a table that had no numeric columns, but received the error: `ERROR:  value overflows numeric format`. Not only did my statement not affect any numeric columns, the table itself didn't have any numeric columns. The actual problem ended up being some malformed json that I was trying to insert into a `jsonb` column. The json had a value like `300e715100` which was actually part of a hashed string, but the json serializer I was using incorreclty identified it as a very large scientific notiation number, and so did not quote it.  Because postgres cannot deal with a number that large it throws the error.  Quoting the value properly fixed the problem.  I also want to note that the error would not happen with `json`, only with `jsonb` because postgres is actually parsing the document.

{% highlight sql %}
select '{"v": 300e715100}'::jsonb;
-- ERROR:  value overflows numeric format
-- LINE 1: select '{"v": 300e715100}'::jsonb

select '{"v": 300e715100}'::json;
-- this statement executes without error.
{% endhighlight %}

You can try the code and see the error for yourself here: [http://dbfiddle.uk/?rdbms=postgres_9.6&fiddle=1584330f148ab0e9ed72529dfb466a12](http://dbfiddle.uk/?rdbms=postgres_9.6&fiddle=1584330f148ab0e9ed72529dfb466a12)
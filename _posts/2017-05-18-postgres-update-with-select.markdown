---
layout: post
title:  "Postgres update using subselect"
date:   2017-05-18 12:00:00
author: Ryan Guill
categories: postgresql sql
tags:	postgresql sql
---

Today I learned that postgres allows you to use a subselect in an update statement using a special syntax.  This allows you to update a record from other data in the system easily (without remembering the weird update-with-join syntax) or to have an update syntax that more closely resembles an insert statement.  For example:


{% highlight sql %}
UPDATE table
SET (foo, bar) =
(SELECT 'foo', 'bar')
WHERE id = 1;
{% endhighlight %}

The subselect can be any query, just return your columns in the same order as the column list you provide.  Here is the relevant documentation if you want to read further: [https://www.postgresql.org/docs/current/static/sql-update.html](https://www.postgresql.org/docs/current/static/sql-update.html)

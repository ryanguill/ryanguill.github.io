---
layout: post
title: "My PostgreSQL wishlist"
date: 2024-01-03 12:00:00
author: Ryan Guill
categories: postgresql sql database
tags: postgresql sql database
---

<style>
  dt {
    font-weight: bold;
    margin-top: 15px;
  }
  dd {
    margin-bottom: 10px;
  }
  h2 {
    margin-top: 10px;
  }
</style>

If you know me you know that I love SQL and relational databases. And of all of the databases I have used, PostgreSQL is by far my favorite. I've stated before that SQL is the one technology I have seen in common across every job I have had over the past two decades. I would bet you could say the same - even if you aren't writing it directly (which would be a shame in my opinion), its still there, behind the scenes, handling all of your data. But if you're fortunate enough to really work with SQL, with PostgreSQL directly, you would be hard pressed to find a better tool.

But while I have never seen a better database than PostgreSQL (and you can't beat the price!), that doesn't mean that there aren't things that could be improved. My goal with this post is to start a conversation and throw out some ideas that I have gathered over the years of things I yearned for. Best case scenario, someone tells me that these things already exist and I learn something new! Second best, these ideas resonate with others and we find ways to get some of these in future versions. But I would also love any conversation about why any of these are bad ideas or technically infeasible - I'll learn something then too. And if anyone has ideas about how I can contribute to these things directly, please let me know!

<!-- break -->

This list is somewhat organized into sections and subsections, but is not really in any order of importance of ease of implementation at all.


<h2>DDL Enhancements</h2>
So lets start with DDL, how we create and manage our schema. Gotta start this section off with praise for transactional DDL - if you have ever worked without it you'll know how amazing it is. But I find myself wanting more, especially around describing the schema in more detail, and using that to generate or check code using the schema. So lets get started:

<dt>I wish I could set a column as being insertable, but not updatable, so immutable.<dt>
<dd>There are times where I want to have a column able to be written to on insert, but immutable from then on. There are ways to do this with triggers, or permissions but I want to be able to specify this on the schema itself, to be able to retrieve that a column is immutable.<br><br>

Bonus points if I could say that it could be inserted as null, and updated from null, but not updated if the value is anything other than null.</dd>

<dt>I wish I could set a column to be generated on update.</dt>
<dd>The easiest example here would to set an updated_at column automatically if a row is updated in any way, but without having to specify it. I want to be able to do this when I create (or alter) the table, but never have to think about it again. <code>created_at</code> is easiest enough with a default value. But would be better if it could be made immutable.</dd>

<!-- <br>
<h3>Foreign Keys</h3> -->

<dt>I wish I could have a "weak" or optional foreign key.</dt>
<dd>Something like <code>REFERENCES foo ON DELETE IGNORE</code><br>
I want to be able to say that if this key exists, its in this table, but it might not exist any longer.<br>
The easiest example here would be for an audit log. The FK ties to the underlying table, but if the record for the underlying table is deleted I wouldn't want anything to happen to the data in the audit log.<br>
I could see a use for a version that checks that the reference row exists at time of insert but then is ignored after that, and a version that doesn't care at all, I just want to be able to describe in my schema that this is how these tables are related (and you probably want to use an outer join).
</dd>

<dt>I wish I could have a foreign key that used an operator other than equality.</dt>
<dd>I think if this was possible it would open up several possibilities, but the main motivation here for me is bitemporal tables. I want to have a FK that takes an ID and a timestamp in one table, and ties it to that a row existing in the target table with the same ID and a timestamp range that includes my timestamp. I have a whole set of articles coming on bitemporal modeling in postgres and this would be amazing for that work.</dd>

<dt>I wish that when you created a foreign key that it would create an index on the target column by default, and if necessary give a way to opt out of it.</dt>
<dd>This is a very common source of performance problems, and one that surprises a lot of developers coming from other databases.</dd>

<dt>I wish I could assert a non-empty constraint the same way I assert a not null constraint.</dt>
<dd>I can do this with check constraints, but I wish it was something described in the schema itself. And you could take this further, assert that it must be a certain length (or range of lengths), or match a certain regex. But I want this in the schema so it is available to codegen tools.<br>
I'm certain you could do this too with custom types, but those are also very opaque to the schema. I want something that is easy to build other tools on top of.</dd>


<dt>I wish you could specify JSONBArray vs JSONBObject vs JSONB.</dt>
<dd>A common constraint is to say that a JSONB column must be null or an object, most of the time if you are working with json columns its either an array or an object, not both.</dd>

<dt>I wish you could specify in the schema that view columns were not null.</dt>
<dd>All view columns are forced to be nullable, even if they aren't really. I don't know how you could do this or what the syntax should look like, but its frustrating to have all columns in a view be nullable. PG should be smart enough to figure out if its possible in most if not all cases.</dd>

<dt>I wish you could alter the definition of an existing generated column.</dt>
    <dd>
        Columns change, it shouldn't require you to drop and recreate a column. I might want to leave previously generated data alone and change the definition going forward.
    </dd>

<dt>I wish you could do something like CREATE INDEX CONCURRENTLY IF AVAILABLE ...</dt>
<dd>
    It's a common problem that I run migrations inside of a transaction where possible, but I want to be able to copy those same statements and run them manually if necessary to get concurrent index creation. I just want to make the syntax of the statement work in either situation.
</dd>

<h3>Schema Metadata</h3>
This section is a little more abstract, so I want to give an introduction to my perspective. My goal is to be able to describe and understand my schema, both manually but also with tools. There are patterns, conventions, and other approaches we bring to our databases that we aren't currently able to describe. And there is many times that we are doing exploratory analysis on a database and its data, and there are things we can do to aid in that understanding. Such as:
    
<dt>I wish that we could control the default order of columns without having to rewrite the table.</dt>
<dd>Store this order separate from the schema itself. I don't care how it is stored on disk. I want to be able to add a new column to a table near the beginning, so it that is obvious to anyone who comes and explores.<br>
Similarly, I wish I could "group" (not that group, no pun intended) columns together with metadata.<br>
As an example, I want to create a column group called "name" that is actually multiple columns, like salutation, first, last, middle, suffix, etc.<br>
I want this mostly for documentation purposes, but this would be even more amazing if you could select the column group and get all columns in the group.<br>
</dd>

<dt>I wish columns could be case insensitive, but created as mixed case, stored that way so that codegen could use the mixed case, but retrieved using any case.</dt>
<dd>Basically what it does now, store it as lowercase on disk, but keep a mapping to the way it was created (and allow it to be altered), and return the mapped column name when returning results unless an alias is specified.
</dd>

<dt>I wish we had better hash indexes</dt>
<dd>
    There were updates in a relatively recent version to make them crash safe, which was a great step in the right direction, but we still can't use them as a unique key. We use UUIDs, IMO it should be the default. For the vast majority of cases, a btree index still works just fine, but it has things we don't need. A hash index would be perfect for indexing UUIDs.
</dd>

<h2>DQL Enhancements</h2>
These would be the crowd pleasers I believe

<dt>I wish I was not required to specify a GROUP BY clause for most aggregate queries.</dt>
<dd>Why must I group by columns manually? Why can't the default for a query such as SELECT COUNT(*), name FROM data not automatically know that I want to group by name? It gives me an error that I must do something with name, so it knows that it is missing. I could group by more than name, but this is rare.<br>
But if not this, then supporting GROUP BY ALL like some other databases like duckdb or snowflake would still be a welcome improvement.<br>
I can concede that this might be confusing for beginners to SQL. But in all the years that I have taught SQL, this is the number one confusing thing already.<dd>


<dt>I wish I could use <code>ORDER BY ALL</code>.</dt>
<dd>Order by the columns ascending in the specified order. Like duckdb</dd>

<dt>I wish I could use column aliases in <code>WHERE</code>/<code>HAVING</code></dt>
<dd>Like duckdb, We can do this with <code>GROUP BY</code> today, but not in a <code>WHERE</code> or <code>HAVING</code> clause.<br>

This may be my number one thing on the entire list. I am a column preceding kind of guy. But even if you're the opposite, I bet youve wished for this too:
<dt>I wish I could have leading and trailing commas for column lists!</dt>
<dd>Please, allow these two queries to be valid:

{% highlight sql %}
SELECT
  , a
  , b
FROM foo;
 
SELECT
  a,
  b,
FROM foo;
{% endhighlight %}

</dd>

<dt>I wish that multiple WHERE clauses were treated as AND conditions.</dt>
<dd>A frequent pattern of mine is to write analytical queries like this:
{% highlight sql %}
SELECT
 ...
FROM foo
WHERE true
--AND condition = false
AND other_condition
AND yet_another_column = 'bar'
{% endhighlight %}

This lets me comment out conditions during testing. I wish I could instead do things like

{% highlight sql %}
SELECT
 ...
FROM foo
WHERE condition = false
-- WHERE other_condition
WHERE yet_another_column = 'bar'
{% endhighlight %}

<dt>I wish that there was an EXCEPTION JOIN.</dt>
<dd>I used this in DB2 decades ago. Select from the left table where there is no matching row in the right table. Basically the same thing as:

{% highlight sql %}
SELECT
...
FROM a
LEFT OUTER
  JOIN b
  ON a.b_id = b.id
WHERE b.id IS NULL
{% endhighlight %}

But far more explicit:

{% highlight sql %}
SELECT
...
FROM a
EXCEPTION
  JOIN b
  ON a.b_id = b.id
{% endhighlight %}
</dd>

<dt>I wish there was a "percent" function built in.</dt>
<dd>I could totally write this as a custom function and have, but I wish it was there by default. Something like: <code>round((a / nullif(b::**numeric,0)) * 100, 2)</code></dd>


<dt>I wish that if you used an INNER JOIN on a table with a clause using = that it would understand that the values in those columns must be identical, so that it wouldn't treat that column name as ambiguous.</dt>
<dd>It is able to do this today if you use a NATURAL JOIN (which I've never once seen in the wild and don't really recommend), so I believe this should be possible.</dd>


<h2>Miscellaneous</h2>
<!-- <h3>UUIDs</h3> -->

<dt>I wish we had more uuid types.</dt>
<dd>uuid v4 / v5 are great. But theres lots of other implementations out there including ones that are smaller in length. It would be awesome to have more options, and for them to be built in and not require an extension.</dd>

<dt>I wish that the conversion from uuid to text could be automatic.</dt>
<dd>And I wish that the planner could be smarter with this and pick better indexes.<br>
See also HASH INDEXes above.</dd>


<dt>I wish columns like created_at and updated_at were automatic.</dt>

<dt>I wish that bitemporal features could be built into the database by default.</dt>
<dd>This deserves and will hopefully get its own blog series soon.</dd>

<dt>I wish I could have identifiers longer than 63 characters</dt>
<dd>Its rare, but when naming things well, especially compound things like table + constraint type, it happens. You can recompile PG to get it, but its an unfortunate limitation.</dd>


<dt>I wish there was a built in scheduler. PG_CRON is great, but it should be built in.</dt>
<dd>Similarly, I wish there was a way to define an automatic update frequency on a materialized view.<br>
Or better yet, create implicit dependencies on the tables and possibly rows (where filter) that he db can detect that the source has updated and it automatically updates the materialized view.</dd>


<dt>I wish I could use hints.</dt>
<dd>Sometimes I want to force PG to use an index. Let me select it, let the performance to be bad and let me understand why the planner isn't using that index. Bonus points if could tell me why it didn't use that index in the first place in plain english.</dd>


<dt>I wish I could easily set an identifier when starting a transaction and have that identifier automatically added as metadata to the row as who inserted and updated the row last.</dt>

<dt>I wish I could have nested transactions.</dt>

<dt>I wish I could create a point in time and roll back to that point in time, regardless of transactions.</dt>
<dd>This would be amazing for unit tests. Let me set the DB into a known state, set a save point, run a bunch of statements, and then throw everything away after the save point.<br>
Even if this required putting the database into a single user mode or similar, this would be so valuable.<br>
</dd>


<dt>I wish there were different storage engines similar to mysql, specifically I want to have a columnar store format in PG.</dt>
<dd>This is huge, I know, but it would be so so valuable, and look at all of the columnar stores out there that are popping up.</dd>


<dt>I wish we could have new ways to compose queries.</dt>
<dd>Allow me to create functions like query partials that can be named and composed. Similar to macros. Look at what DBT is doing and steal most of it.</dd>

<dt>This could have really been in the DQL section but I wish we could build a query pre-processor that would let us implement extensions and experiments on top of SQL.</dt>
<dd>This is a bigger thing, so let me explain. There are many things that require different syntax to achieve. Things like the composition functions I mention above, or things like <code>GROUP BY ALL</code> or <code>ORDER BY ALL</code>. These are things we should be able to extend ourselves, but we need a place to put this pre-processor in a place that all of the ways we talk to the database can go through. So best case scenario, thats the database. Make us include a pragma or similar at the beginning of the query and opt into using it. But imagine if we could instead write a query like this:<br>

{% highlight sql %}
FROM table
INNER
  JOIN other_table
  ON table.x = other_table.x
WHERE
  NOT condition
SELECT
  , x
  , count(*) n
ORDER BY ALL
{% endhighlight %}

This would be so much easier to teach people how to reason about SQL. You could run everything up to the <code>WHERE</code> clause, leaving off the <code>SELECT</code> and have it transformed into <code>SELECT *</code>. A pre-processor would allow you to explore these alternative syntaxes and see how they really work. Or build your own DSLs that get turned into standard SQL.<br>
Bonus points if its a full environment that has access to all of the schema (and the extensions ive wished for) and can not just transform but build queries.<br>

<dt>And last but not least, I wish we had a standard AST parser.</dt>
<dd>Let me use the parser built into PG and get out a standard AST that we can use for formatting, transformation, or knowing what queries are touching what parts of the schema. There are many use cases for this.<dd>

<h2> Conclusion</h2>

I want this to be a living document. I can't wait for someone to tell me how wrong I am in the comments. When that happens I'll update this list. And tell me what you thing I missed, the things you wish for - I'll add new ideas as well. And will be very happy to celebrate when any of these are addressed in PostgreSQL! I really hope this post is received in the spirit it is intended - the only reason I am making this post is because I believe and have seen amazing new capabilities added to PG over the years. PG release notes are one of my favorite things! These are not at all intended to be criticism. There are many many years of reasons why things are the way they are. But PG has so much potential to be bigger and better than it already is.

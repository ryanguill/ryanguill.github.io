---
layout: post
title:  "Partitioning using UUIDs"
date:   2024-08-09 12:00:00
author: Ryan Guill
categories: postgresql sql uuid
tags:	postgresql sql uuid
---
Recently I had a situation where I needed to process quite a few records, lets say around 100k, and the processing of each record was around 2 seconds. The math on that wasn't very pretty, so I needed to partition the set of data so that I could run multiple instances of the processing at the same time - but where each instance would have their own data and I wouldn't try to process a record by more than one instance.

Normally you would want to look for some natural key if you can, but in this case there wasn't anything I could use, especially that would be well distributed. I also wanted to have the flexibility to partition for as few or as many instances as I needed - I might start with 5 instances but that might not be enough.

The one thing I do have are UUIDs. We use UUIDs for virtually all of our keys - an explanation of all of the benefits of that will have to be its own blog post someday.

So I had the thought to use UUIDs to do the partitioning. The easiest thing you could do is look at the last character, that would quickly give you 16 partitions without much work, and most of the versions of UUIDs the last character would be fairly well distributed.

But then I remembered - a UUID is really just a 128 bit number, or two 64 bit integers (bigints) in a trench coat - and assuming they are randomly generated (we use v4 for most things right now so I know they are), I can use modulus math to partition into however many buckets I need.

I was able to come up with the following that given a UUID will extract the high bigint and then give mod 5:

```sql
SELECT abs(('x' || translate(gen_random_uuid()::text, '-', ''))::bit(64)::bigint % 5)
```

This might look complicated at first, but while it has a few steps its fairly straight forward. A few things to notice first:

A UUID is a hex encoded number that has hyphens in particular places to break it up into pieces that make it a little easier to read.  So to break it apart and pull out just the higher piece:

a) convert the uuid to text

b) remove the hyphens

c) prepend an 'x' to the beginning of the string - this gives us a string of hex characters that can be understood as hex encoded

d) convert that to a bit string using `::bit(64)` - this part uses a fact that if you take a number bigger than a bit type can hold it will just take as much as can fit and throw away the rest, so this will only take the first 64 bits

e) take that 64 bits and convert it to a bigint using `::bigint`

f) lastly take its absolute value because the number is signed and you might get a negative, but that doesnt matter for our purpose

With these steps done you only need to use `%` to take the modulus of that number and get the remainder. You can change 5 to whatever number you want to get the number of buckets - just remember that the answer will be zero based. If you use `% 5` you will get 0 through 4 as possible answers.

Now when I create my instances I only have to put in the number of partitions and which partition this instance is working with, and a simple where clause in the query to get the population it is working on will restrict it to only the records that belong to that instance and no two instances will try to do the same work.

For clarity, here is what this might look at in use:

```sql
SELECT
  id
  , ...
FROM foo
WHERE abs(('x' || translate(id::text, '-', ''))::bit(64)::bigint % 5) = 2
```

If you're interested in exploring more about how UUIDs split into numbers and back again or proving to yourself that a random uuid is evenly distributed, you can check out this fiddle: [https://dbfiddle.uk/yX-y7Ath](https://dbfiddle.uk/yX-y7Ath)

And one more bonus fact related to UUIDs - MD5 hashes are also 128 bit numbers stored as hex, and since UUIDs are also just 128 bit numbers stored as hex, you can convert MD5 hashes to UUID and store them using the UUID type in your database for space savings compared to storing it as text.

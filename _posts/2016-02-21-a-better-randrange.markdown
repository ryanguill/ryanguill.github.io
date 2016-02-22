---
layout: post
title:  "A Better RandRange()"
date:   2016-02-21 12:00:00
author: Ryan Guill
categories: CFML math
tags: CFML math randrange
---

Every CFML engine I can find - Adobe ColdFusion 10, 11 and 2016, Lucee 4.5 and 5 - has a bug where if you try to use `randRange()` on 2<sup>31</sup>-1 (`MAX_INT`) it will overflow and give you a negative number.  See for yourself: [http://trycf.com/gist/726e96e5c5e9498b32a2/acf2016](http://trycf.com/gist/726e96e5c5e9498b32a2/acf2016).  Here is a better way that supports not only `MAX_INT` but also `MAX_LONG` (2<sup>63</sup>-1).
<!-- break -->

{% highlight text %}
<cfscript>
function randRangeInt (min, max) {
	return createObject("java", "java.util.concurrent.ThreadLocalRandom").current().nextInt(min, max);
}

function randRangeLong (min, max) {
	return createObject("java", "java.util.concurrent.ThreadLocalRandom").current().nextLong(min, max);
}

//old and busted
writedump(randRange(0, 2147483647)); //negative!
writedump(randRange(0, 2^31-1)); //negative!

//the new hotness
writedump(randRangeInt(0, 2147483647));
writedump(randRangeInt(0, 2^31-1));
writedump(randRangeInt(0, 2147483646));
writedump(randRangeInt(0, 2^31-2));

writedump(randRangeLong(0, 9223372036854775808));
writedump(randRangeLong(0, 2^63-1));
</cfscript>
{% endhighlight %}

Note: this requires java 1.7+. Relevant bugs in [ACF (closed of course)](https://bugbase.adobe.com/index.cfm?event=bug&id=3041752) and [Lucee](https://luceeserver.atlassian.net/browse/LDEV-25).  Both are over a year old.

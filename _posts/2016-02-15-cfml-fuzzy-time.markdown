---
layout: post
title:  "CFML Fuzzy Time"
date:   2016-02-15 12:00:00
author: Ryan Guill
categories: CFML
tags: CFML
---

A friend asked recently how I would go about writing a function to do fuzzy time - something that formats time in a general way, the way you would talk about it in conversation - "just now", "a few minutes ago", "2 days ago", etc.  He wanted it to be customizable, where they could define the groupings used.  This is what we came up with:
<!-- break -->

{% highlight cfm %}
<cfscript>

	/**
	 * Displays a formatted approximation of how long ago a timestamp was.
	 *
	 * @param input - Date to Format (required)
	 * @param defaultMask - the date mask if the date is earlier than the earliest case.  Default dd MMM, YYYY
	 * @return Returns a string.
	 * @author Ryan Guill (ryanguill@gmail.com), Adam Tuttle (adam@fusiongrokker.com)
	 * @version 1, Sept 11, 2014
	 *
	 * To customize, add a struct to the map for your case.  Order matters, cases are
	 * evaluated in order, the first one that matches will be used.  In the structure,
	 * n is the amount, p is the datepart (see dateDiff for options), and m is the message.  
	 * You can use {x} for the amount and {s} for an optional pluralization of the
	 * message if the amount != 1;
	 *
	 * ACF 9+
	 *
	 * https://gist.github.com/ryanguill/a0b4bd5092b6044824c9
	 */

	string function fuzzy (required date input, string defaultMask = 'dd MMM, YYYY') {
		var now = now();
		var map = [
			  { n: 60, p: "s", m: "just now" }
			, { n: 60, p: "n", m: "{x} min{s} ago" }
			, { n: 24, p: "h", m: "{x} hr{s} ago" }
			, { n: 2,  p: "d", m: "yesterday" }
			, { n: 7,  p: "d", m: "{x} day{s} ago" }
		];

		for ( var item in map ) {
			var x = dateDiff( item.p, input, now );
			if ( x < item.n ) {
				return item.m.replace("{x}", x).replace("{s}", x == 1 ? '' : 's');
			}
		}
		return dateFormat( input, defaultMask );
	}

	inputs = [
		  dateAdd("s", -1, now())
		, dateAdd("s", -30, now())
		, dateAdd("n", -1, now())
		, dateAdd("n", -30, now())
		, dateAdd("d", -1, now())
		, dateAdd("d", -15, now())
		, dateAdd("m", -1, now())
		, dateAdd("m", -2, now())
		, dateAdd("m", -11, now())
		, dateAdd("m", -15, now())
		, dateAdd("yyyy", -1, now())
		, dateAdd("yyyy", -5, now())
		, dateAdd("yyyy", -50, now())
	];

</cfscript>

<cfoutput>

	<cfloop array="#inputs#" index="input">
		#input#: #fuzzy(input)#<br />
	</cfloop>

</cfoutput>
{% endhighlight %}

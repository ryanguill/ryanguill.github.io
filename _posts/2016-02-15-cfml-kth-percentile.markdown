---
layout: post
title:  "kth Percentile in CFML"
date:   2016-02-15 12:00:00
author: Ryan Guill
categories: CFML
tags: CFML statistics
---

I recently needed to analyze some data in CFML where there was a wide range of values but some real outliers - latency numbers for example.  So I ported this `kthPercentile()` function.  You pass in the percentile and an array of numbers - `kthPercentile(99, [...])` will give you the 99th percentile for example - `kthPercentile(50, [...])` is the same as the median.

{% highlight text %}
<cfscript>
	function kthPercentile (k, data) {
		if (k > 1) { //this allows users to pass in .99 or 99
			k = k / 100;
		}
		arraySort(data, "numeric");
		var kth = k * arrayLen(data);
		if (kth == ceiling(kth)) { //its a whole number
			return data[kth];
		} else {
			return (data[int(kth)] + data[ceiling(kth)]) / 2;
		}
	}
</cfscript>
{% endhighlight %}

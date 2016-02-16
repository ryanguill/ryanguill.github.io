---
layout: post
title:  "CFML Value Array"
date:   2016-02-15 19:00:00
author: Ryan Guill
categories: CFML
tags: CFML
---

Occasionally in the [CFML Slack channel](http://cfml-slack.herokuapp.com/) (and the IRC room before it) someone asks about a [`valueArray()`](http://cfdocs.org/valuearray) function - what they really mean is that they want something like the terribly named [`valueList()`](http://cfdocs.org/valuelist) that you can provide a query and a column and get a column slice but something that returns an array instead of a CFML list.  `valueArray()` [exists on Lucee](http://docs.lucee.org/reference/functions/valuearray.html) but for ACF you're stuck implementing it for yourself.  Here is a way to do that properly (it's easy to do it naively wrong).

<!-- break -->

{% highlight text %}
// ACF only, lucee already has a valueArray function
function valueArray (required query q, required string column) {
	var output = [];
	output.addAll(q[column]);
	return output;
}
{% endhighlight %}

This requires dropping down into java reflection territory, but the benefit is that it actually adds things to the array directly, value by value. This means that everything works no matter what the value is - commas in the values are problematic for using `valueList()` and then something like `listToArray()`.

You can see it in action [on trycf](http://trycf.com/gist/45481a49c17e95872523).

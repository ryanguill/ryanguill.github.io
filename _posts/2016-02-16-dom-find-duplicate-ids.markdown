---
layout: post
title:  "Find duplicate IDs in your DOM"
date:   2016-02-16 12:00:00
author: Ryan Guill
categories: js html dom
tags:	js html dom
---
With a dynamic application with lots of shared templates it can sometimes be easy to use the same ID for two different elements on the same page.  Sometimes this can manifest itself by your JS not working quite right but it isn't apparent what the problem is.  Here is a quick script you can paste into your console to report any duplicates.

{% highlight js %}
var allElements = document.getElementsByTagName("*"), allIds = {}, dupIDs = [];
for (var i = 0, n = allElements.length; i < n; ++i) {
  var el = allElements[i];
  if (el.id) {
  	if (allIds[el.id] !== undefined) dupIDs.push(el.id);
  	allIds[el.id] = el.name || el.id;
    }
  }
if (dupIDs.length) { console.error("Duplicate ID's:", dupIDs);} else { console.log("No Duplicates Detected"); }
{% endhighlight %}

Math Busche covered the same topic last year, [head over there](http://matthewbusche.com/blog2/2015/04/13/checking-an-html-page-for-duplicate-ids-using-javascript/) to see how he tackled the same thing.

---
layout: post
title:  "Setting a minimum request timeout in CFML"
date:   2016-02-17 12:00:00
author: Ryan Guill
categories: CFML
tags: CFML
---

You rarely want to set a request timeout to a particular value - meaning that you want it to time out if it takes a certain amount of time.  What you do want is to declare that a particular process might take at least some amount of time to complete.  This is what `<cfsetting>`'s requestTimeout parameter should be - saying that it is ok if it takes _at least_ this long.  A recent example of where I needed this is with running some longer running processes as part of a suite of unit tests.  The individual method we are testing might take 60 seconds to run for example - but the entire request might take several minutes - when that method is run as part of a normal request lifecycle then the 60 second request timeout is fine, but when running the unit tests it ends my tests early!

So here is a method that you can use instead - that will update the request timeout to be the greater of the existing timeout or the new timeout.  So it will only ever extend, never shorten.

{% highlight text %}
<cfscript>
  function setMinimumRequestTimeout (required numeric timeout) {
    var currentTimeout = 0;
    try {
        var requestMonitor = createObject("java", "coldfusion.runtime.RequestMonitor");
        currentTimeout = requestMonitor.getRequestTimeout();
    } catch (any e) {
        //do nothing
    }
    var newTimeout = max(currentTimeout, arguments.timeout);
    writedump(var="setting requestTimeout to #newTimeout#");
    setting requestTimeout=newTimeout;
  }

  setMinimumRequestTimeout(10); //if the timeout is 60 seconds it will not be updated
  setMinimumRequestTimeout(1000); //the timeout will be updated to 1000s

</cfscript>
{% endhighlight %}

Credit to [Brian Ghidinelli](http://www.ghidinelli.com/).

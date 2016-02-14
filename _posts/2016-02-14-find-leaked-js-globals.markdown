---
layout: post
title:  "Find leaked JS globals"
date:   2016-02-14 12:00:00
author: Ryan Guill
categories: js
tags:	js
---

It can sometimes be easy to inadvertently leak variables / functions into the global scope in your client side javascript - this one-liner will report all non-browser global keys and their values on the page - just paste into your chrome console.

{% highlight javascript %}
keys(window).filter(function(key){ return ["location","document","window","external","chrome","top","lastpass_iter","lastpass_f"].indexOf(key) == -1;}).forEach(function(key){console.log(key, window[key]);});
{% endhighlight %}

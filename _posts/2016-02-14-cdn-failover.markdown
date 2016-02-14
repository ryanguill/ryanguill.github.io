---
layout: post
title:  "CDN Failover"
date:   2016-02-14 12:00:00
author: Ryan Guill
categories: js cdn
tags:	js cdn
---

For most sites you want to get the benefits of a CDN, but it is still a single point of failure.  I came across this pattern recently though that allows you to fail over to a local file if the CDN library doesn't load.  Would probably have to take a different approach with CSS libraries though.

{% highlight html %}
<!-- try to download from CDN -->
<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>
<!-- if failed, switch to local copy -->
<script>window.jQuery || document.write('<script src="local_server_path/jquery.min.js"></script>')</script>
{% endhighlight %}

Something I hope to explore more very soon is webpack, which might make this trick obsolete.

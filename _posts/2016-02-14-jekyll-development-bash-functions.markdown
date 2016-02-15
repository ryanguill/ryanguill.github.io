---
layout: post
title:  "Jekyll Bash Function"
date:   2016-02-14 12:00:00
author: Ryan Guill
categories: bash jekyll
tags:	bash jekyll
---

Trying to streamline my Jekyll development workflow, I came up with this function that I have added to my `~/.bash_profile` to make things just a bit easer.

{% highlight text %}
jserve() {
	cd ~/dev/ryanguill-blog
	/usr/bin/open -a '/Applications/Google Chrome.app' 'http://localhost:4000'
	bundle exec jekyll serve
}
{% endhighlight %}

Obviously you will need to change the cd at the beginning of `jserve`, but this will start the Jekyll process and open up a new tab in chrome to the test address. I tried to use the detached mode for jekyll, but apparently there has been a bug for a long time that detached mode doesn't also watch the directory so that was a non-starter.  The only problem with this is that the tab will open before the serving starts, but if you wait just a second and then refresh the page it should be ready to go.

I'm no bash expert though so if anyone has any improvements or other ideas I would like to hear about them.  

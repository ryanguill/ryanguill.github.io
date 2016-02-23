---
layout: post
title:  "CFML Base62 Library"
date:   2016-02-22 12:00:00
author: Ryan Guill
categories: CFML
tags: CFML base62
---

Want to build your own URL shortener? Have a bunch of sequential ID's but don't want it to be obvious what the next or previous in the sequence is? Base62 might be a good fit. Instead of 10 possible characters per digit you have 62, compressing the size of your identifier.  Plus with a custom alphabet order, the next number in the sequence isn't easily apparent.  I have open sourced a CFML library that allows you to convert between base 10 and 62 here: [https://github.com/ryanguill/cfmlBase62](https://github.com/ryanguill/cfmlBase62) - it supports custom alphabets (will also help generate one for you) and supports integers between 0 and 2<sup>63</sup>-1 (9,223,372,036,854,775,807) so it can probably handle all of the nine quintillion identifiers in your database.
<!-- break -->

{% highlight text %}

base62 = new Base62();
base62.fromBase10(123); //b9
base62.toBase10("b9"); //123

{% endhighlight %}

There is a [complete set of tests](https://github.com/ryanguill/cfmlBase62/tree/master/tests). See [here for some more example usage](https://github.com/ryanguill/cfmlBase62/blob/master/tests/basicTest.cfc#L9) or [here to see a custom alphabet being used](https://github.com/ryanguill/cfmlBase62/blob/master/tests/customAlphabet.cfc#L8). Supports Lucee 4.5+ and ACF 10+.  Pull requests and issues welcome!

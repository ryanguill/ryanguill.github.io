---
layout: post
title:  "Going Further with Map"
date:   2016-05-22 12:00:00
author: Ryan Guill
categories: functional higher-order-functions
tags:	functional higher-order-functions map-reduce
cover:  "/assets/js_code.jpg"
---

Previously we discussed [Map, Reduce and other Higher Order Functions](/functional/higher-order-functions/2016/05/18/higher-order-functions.html) (go read that first if you haven't already).  This time lets focus specifically on map, talk a little more about the tasks for which it is well suited and the ones that it is not and look at more real world examples. Once again the examples are in JavaScript (es2015) but the concepts are universal.

I think a good place to start is to demystify map by showing that as a function itself it isn't all that special - in fact if your language of choice does not provide `Map` as part of its standard library but does provide First Class Functions, you can implement it yourself without much trouble.  Lets take a look at an (admittedly naïve) implementation:

todo: example: map as a standalone function

todo: talk a bit about the example

todo: show example of using the standalone map function

JavaScript since es5 has provided a `Map` function as [part of the `Array.prototype`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) and here is [a well explained polyfill version](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map#Polyfill).

Other libraries have also provided version of `Map`, not just for arrays but also other collection types such as object.  Lodash is probably the most notable of these ([documentation](https://lodash.com/docs#map)).


In my previous entry I focused specifically on pure functions for a few reasons.  They are easier to reason about than their impure counterparts and they are certainly what you want to strive for if you have the option.  But functions given to higher order functions don't have to be pure and there are certainly very useful things you can do with impure functions as well.



quick digression into currying
example: recordset to table rows
example: array of ids to records
example: map function composition map(a).map(b) == map(b(a(x))

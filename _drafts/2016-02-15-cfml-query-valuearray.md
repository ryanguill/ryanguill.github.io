---
published: false
---

## CFML Value Array

Occasionally in the CFML Slack channel (and the IRC room before it) someone asks about a [`valueArray()`](http://cfdocs.org/valuearray) function - what they really mean is that they want something like [`valueList()`](http://cfdocs.org/valuelist) that you can provide a query and a column and get a column slice but something that returns an array instead of a CFML list.  `valueArray()` [exists on Lucee](http://docs.lucee.org/reference/functions/valuearray.html) but for ACF you're stuck implementing it for yourself.  Here is how to do that properly (it's easy to do it naively wrong).

> Side note, these functions are terribly named...

```
	// ACF only, lucee already has a valueArray function
function valueArray (required query q, required string column) {
	var output = [];
	output.addAll(q[column]);
	return output;
}
```

This requires dropping down into java reflection territory, but the benefit is that it actually adds things to the array directly, value by value.  This means that everything works no matter what the value is - commas in the values are problematic for using `valueList()` and then something like `listToArray()`.

You can see it in action here: http://trycf.com/gist/45481a49c17e95872523



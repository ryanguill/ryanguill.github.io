---
layout: post
title:  "Map, Reduce and other Higher Order Functions"
date:   2016-05-18 12:00:00
author: Ryan Guill
categories: functional higher-order-functions
tags:	functional higher-order-functions map-reduce
---

There are few things I have learned in my programming career that have paid off like higher order functions.  `Map`, `Reduce` and `Filter` with their cousins, along with the concept of passing functions as data in general make code easier to reason about, easier to write, easier to test.  I find myself evangelizing these concepts often, so I thought I would try to do my best to give an introduction of them, along with some real world examples of how they can improve your everyday programming life.  These examples are in JavaScript, but the concepts are universal.

<!-- break -->

## Terminology

Let's go over just a bit of terminology before we begin to make sure everyone is on the same page. If you read this article and there are any other terms you don't understand, or need a further/better explanation for, let me know in the comments and I will try to either expand on them here or link to better resources.

#### First Class Function

A language that has first class functions is one where you can assign a function to a variable and pass that function around like data. Without first class functions you cannot have higher order functions - usually if you have one you have the other as well. 

#### Higher Order Functions

A higher order function is a function that either takes another function as an argument or returns a function.  That's pretty much it - it's all about functions as data.  Once you have a reference to a function in a variable and can pass it around or return it, many things become possible.  `Map` and `Reduce` and the other higher order functions we discuss are certainly not the only ones - you can create your own higher order functions.  These are just common examples of them that are also commonly baked into the standard libraries of many languages.  These functions we will discuss are generally not special either, you could write your own version of them without too much trouble - they are notable because they are solutions to common problems in everyday programming, no matter what the domain.

#### Pure Functions

A pure function is one that given the same inputs will always return the same output, with no side effects.  An example might be `(a, b) => a + b;`. No matter what you provide as `a` and `b`, if you give them again you will get the same answer.  The function doesn't do anything else either - no side effects means no writing to a database, or logging, or _mutating state_, just takes inputs, gives outputs, and what goes in deterministically directs what comes out.

There are many benefits to pure functions, most of which I will not go into, but some include cacheability, portability (reuse), self-documenting, testabilty.  Pure functions are a unit tester's dream! You can't make an (interesting / useful) system with only pure functions, it wouldn't really do anything - but you should strive to use pure functions wherever possible - sequester your state manipulation in as few places as possible.

Higher Order Functions do not _require_ you to use pure functions, but that is what you will use most of the time and you should always try to use pure functions when possible.

## Map

Map is one of the most common and most useful higher order functions, so let's start there.  Let's say I have a collection of data, and I need to perform some sort of transformation on it. Common examples might be taking complex data and formatting it for output, or plucking individual parts of data out of a more complicated structure.  Let's take a look at an example.

{% highlight js %}
var data = [
    {id: 1, firstName: "Ryan", lastName: "Guill", email: "ryanguill@gmail.com"},
    {id: 2, firstName: "John", lastName: "Doe", email: "johndoe@example.com"},
    {id: 3, firstName: "Mary", lastName: "Smith", email: "marysmith@example.com"}
];
{% endhighlight %}

Let's say we wanted to get a list of everyone to put in the "to" field for an email, something like `lastName, firstName <email>`.  Traditionally we might write a loop:

{% highlight js %}
var output = [];
for (var i = 0; i < data.length; i++) {
    output.push(data[i].firstName + " " + data[i].lastName + " <" + data[i].email + ">");
}
//["Ryan Guill <ryanguill@gmail.com>", "John Doe <johndoe@example.com>", "Mary Smith <marysmith@example.com>"]
{% endhighlight %}

Pretty standard stuff, but let's take a look at how we might write the same thing with `map`:

{% highlight js %}
data.map(function(item) {
    return item.firstName + " " + item.lastName + " <" + item.email + ">"; 
});
//["Ryan Guill <ryanguill@gmail.com>", "John Doe <johndoe@example.com>", "Mary Smith <marysmith@example.com>"]
{% endhighlight %}

The first thing to notice is that we don't have the loop machinery, no chance to get any of those details wrong, no need to keep track of another variable for the index. The code is much closer to _just the code that matters_. 

But let's change it a bit to illustrate another point.

{% highlight js %}
var toFieldFormat = function(item) {
    return item.firstName + " " + item.lastName + " <" + item.email + ">"; 
};
data.map(toFieldFormat);
//["Ryan Guill <ryanguill@gmail.com>", "John Doe <johndoe@example.com>", "Mary Smith <marysmith@example.com>"]
{% endhighlight %}

This makes it clearer that `Map` takes a function, one that has the following argument signature: `function (element [, index] [, collection])`.  We won't go into detail with the other parameters, you generally don't have to use them.  Index can be useful in some cases, but generally speaking if you are using the collection argument in a `map` call, you're probably doing it wrong.

Back to the example, `toFieldFormat` is just a function (a pure one) that takes an input of an object and returns a string as output.  That's it.  We could call it directly:

{% highlight js %}
toFieldFormat({firstName: "Hindley", lastName: "Milner", email: "hindley@example.com"});
//Milner, Hindley <hindley@example.com>
{% endhighlight %}

and it would work just fine.  We could also write our original loop to use this function:

{% highlight js %}
var output = [];
for (var i = 0; i < data.length; i++) {
    output.push(toFieldFormat(data[i]));       
}
{% endhighlight %}

But now you can see that we have abstracted out the real logic that matters and all that's left is the plumbing.  I don't know about you but im tired of writing loops for most things.  The loop _is not what is interesting_ about this code.  When I come back to it in 6 months, I don't want to read the loop to understand what is happening - I want to get to the meat of what the author is trying to achieve.  

Also, `toFieldFormat` is easily testable! It is a pure function, and abstracted out we can easily pass in a variety of inputs and deterministically check their outputs.  

Let's look at another example - let's say we have our array of data, but we want to get just an array of id's.  That's easy with map:

{% highlight js %}
var pluckId = function(item) {
    return item.id; 
};
data.map(pluckId); //[1,2,3]
{% endhighlight %}

So let's talk a bit more about the intrinsic properties of a mapping operation.  

* Map _translates_ data from one type to another.   Doesn't necessarily mean that the data type changes - but you are changing from one form to another. 
* Map will always return a collection the same size and order as its input. If you map an array of 3 things, you will get an array of 3 elements back, and the first item in the input will always correspond with the first item of the output.
* The result of map is always a new collection - the input collection is _not_ modified.
* Map operations are inherently chainable.  `data.map(...).map(...).map(...)` is a common pattern.
* Mathematically, if using pure functions, `data.map(a).map(b)` is the same as `data.map(a ⋅ b);`. _Don't worry about this right now,_  (and this is not valid JavaScript syntax, it's mathematical) but what it means is that certain libraries can speed up your code by performing optimizations, knowing that they can transform your functions.

We are only scratching the surface of the power and usefulness of `map`. If you take away nothing else from this article, learn and embrace at least this one function.  There are more complicated but elegant abilities built on the foundations of `map` that are outside the scope of this particular article, but that I hope to revisit soon.

Editorial Note: some languages use `collect` or `transform` instead of `map`.

## Filter

After `map`, `filter` is probably one of the most commonly used higher order functions.  You give it some data and a function to use as a "test" for your data - if the element passes it is included in the resulting collection, if not it is excluded.  Let's look at an example:

{% highlight js %}
var data = [
    {userID: 1, name: "Ryan", groups: ["dev", "ops", "qa", "employee"]},
    {userID: 2, name: "Bob", groups: ["ops", "employee"]},
    {userID: 3, name: "John", groups: ["qa", "employee"]},
    {userID: 4, name: "Paul", groups: ["dev", "qa", "employee"]}
];

var isDev = function (user) {
    return user.groups.includes("dev");
};
data.filter(isDev);
//[{userID: 1, name: "Ryan", groups: ["dev", "ops", "qa"]}, {userID: 4, name: "Paul", groups: ["dev", "qa"]}]
{% endhighlight %}

`isDev` is our "test" - it returns true or false, does the user's group contain "dev".  That's all there is to it - your test function needs to always return a boolean (undefined and null in js are considered false, but don't do that).  Your filter function could be much more complicated if you wanted though - as long as it returns a boolean.

{% highlight js %}
var meetsArbitraryRestriction = function(user) {
    return user.groups.includes("qa") && user.name.charAt(0).toLowerCase() === "p";  
};    
data.filter(meetsArbitraryRestriction); //{userID: 4, name: "Paul", groups: ["dev", "qa"]}
{% endhighlight %}

Again, the testing function is a pure function, which means easy to test, and the function is easy to use in other parts of your application's logic.

So properties of `filter`:

* Filter will always return the same type of collection as the input, with fewer than or equal to the number of elements in the input.  
* Filter is used to _remove_ items from a collection that fail the testing function.
* The result of filter is always a new collection - the input collection is _not_ modified.
* Filter operations are also inherently chainable - you can do `data.filter(...).filter(...)` as much as you want, or, more commonly, `data.filter(...).map(...)`

## Some and Every

A few languages use `any` instead of `some`, but `some` and `every` are aggregate functions, in that they take a collection, but they return a true or false.  We aren't going to spend much time on these, but let's take a look:

{% highlight js %}
var data = [
    {userID: 1, name: "Ryan", groups: ["dev", "ops", "qa", "employee"]},
    {userID: 2, name: "Bob", groups: ["ops", "employee"]},
    {userID: 3, name: "John", groups: ["qa", "employee"]},
    {userID: 4, name: "Paul", groups: ["dev", "qa", "employee"]}
];

var isDev = function (user) {
    return user.groups.includes("dev");
};

var isEmployee = function(user) {
    return user.groups.includes("employee");   
};

var isManager = function(user) {
    return user.groups.includes("manager");   
};

data.every(isDev); //false, not everyone is a dev
data.every(isEmployee); //true, everyone is an employee
data.some(isDev); //true, at least one user is a dev
data.some(isManager); //false, no user is a manager
{% endhighlight %}

Hopefully that is pretty straight forward.  The only other thing I will mention is that these functions take advantage of their logic to generally return without having to look at every item in the collection - `every` can return as soon as it hits the first `false` result, `some` can return as soon as it hits the first `true` result.

## Reduce

So now we get to the big one, `reduce`.  For some reason `reduce` seems more opaque to the average developer than the others, and I think that stems from the fact that it is a bit of a swiss army knife of higher order functions. So let's start high level - what is a reduction? All it really means is that it will iterate over the collection, building up a result that will be returned at the end.  That's it in a nutshell.  But as we will see, that generic definition lends itself to many uses.

If you have ever used an aggregate function in SQL, you used a reduction.  If you have ever used `join()` you've used a reduction.  

Let's take a look at what is probably the standard example to get our feet wet:

{% highlight js %}
var data = [1,2,3,4,5];
data.reduce(function(prev, item) {
    return prev + item;
}, 0);
//15
{% endhighlight %}

We just totaled up all the items in our array.  You'll notice that reduce takes an extra argument, and that the function given to `reduce` also takes an extra argument.  Here is the definition:

```
reduce(function(previousValue, item, index, collection) {...}, startingValue);
```

Reduce will iterate over the collection element by element, taking the result of the previous iteration and passing it to the next iteration.  The first element will get the `startingValue`.  This doesn't mean that we can't provide it with useful, reusable pure functions though.  Consider this version of the same example:

{% highlight js %}
var data = [1,2,3,4,5];
var sum = function(a, b) {
    return a + b;  
};    
data.reduce(sum, 0);
//15
{% endhighlight %}

Our `sum` function is perfectly generic, testible, reusable - pure.  

Remember I said that `join` is a type of reduction? Let's take a look at what a generic `join` might look like using `reduce`:

{% highlight js %}
var data = [1,2,3,4,5];
var join = function(a, b) {
    if (a === 'undefined') return b;
    return a + ',' + b;  
};    
data.reduce(join);
//"1,2,3,4,5"
{% endhighlight %}

In this case, we don't pass a starting value, and have our join handle it appropriately.  Now, the native `string.prototype.join` is much better at its job than this, but hopefully this was useful as an illustration.

Let's look at another example, this time let's see if we can find the smallest number out of a set.

{% highlight js %}
var data = [100,250,50,300,450];
var min = function(a, b) {
    return Math.min(a, b);  
};    
data.reduce(min);
//50
{% endhighlight %}

So all of our examples so far have used reduce as an aggregation, getting down to a simpler value from an input collection - but `reduce` can return any kind of value - including a collection.  In fact, it could even return a larger collection than the input.

Let's say that we want to take our users array from earlier examples, and create an element for each user / group combination.

{% highlight js %}
var data = [
    {userID: 1, name: "Ryan", groups: ["dev", "ops", "qa", "employee"]},
    {userID: 2, name: "Bob", groups: ["ops", "employee"]}
];

//just creating this for clarity later
function arrayMerge (arrayOne, arrayTwo) {
    Array.prototype.push.apply(arrayOne, arrayTwo);
    return arrayOne;
}

data.reduce(function(acc, user) {
    return arrayMerge(acc, user.groups.map(function(group) {
        return {name: user.name, group: group};
    }));
}, []);
/*
[{name:"Ryan",group:"dev"},{name:"Ryan",group:"ops"},{name:"Ryan",group:"qa"},{name:"Ryan",group:"employee"},{name:"Bob",group:"ops"},{name:"Bob",group:"employee"}]
*/
{% endhighlight %}

Hopefully this is still clear - as you can see we use map to take our array of groups and return a new array of the same size, but transforming them into objects with the name of the user and the group.  Then we just merge our mapped groups into the array we are building user by user until we end up with the complete result.

So to further bolster the swiss-army-knife analogy, let me show you how all the other higher order functions we have talked about are actually just specialized reductions. `Map`, `Filter`, `Some`, `Every` - all of these can be achieved with `reduce`.

Here is our first `Map` example implemented using `Reduce`:

{% highlight js %}
var data = [
    {id: 1, firstName: "Ryan", lastName: "Guill", email: "ryanguill@gmail.com"},
    {id: 2, firstName: "John", lastName: "Doe", email: "johndoe@example.com"},
    {id: 3, firstName: "Mary", lastName: "Smith", email: "marysmith@example.com"}
];

var toFieldFormat = function(item) {
    return item.firstName + " " + item.lastName + " <" + item.email + ">"; 
};
data.reduce(function(arr, item) {
   arr.push(toFieldFormat(item));
   return arr;
}, []).join(", ");  
{% endhighlight %}

Here is our `Filter` example:

{% highlight js %}
var data = [
    {userID: 1, name: "Ryan", groups: ["dev", "ops", "qa", "employee"]},
    {userID: 2, name: "Bob", groups: ["ops", "employee"]},
    {userID: 3, name: "John", groups: ["qa", "employee"]},
    {userID: 4, name: "Paul", groups: ["dev", "qa", "employee"]}
];

var isDev = function (user) {
    return user.groups.includes("dev");
};
data.reduce(function(arr, user){
    if (isDev(user)) {
        arr.push(user);
    }
    return arr;    
}, []);
//[{userID: 1, name: "Ryan", groups: ["dev", "ops", "qa"]}, {userID: 4, name: "Paul", groups: ["dev", "qa"]}]
{% endhighlight %}

And here is our `Some` and `Every` examples rewritten as reductions:

{% highlight js %}
var data = [
    {userID: 1, name: "Ryan", groups: ["dev", "ops", "qa", "employee"]},
    {userID: 2, name: "Bob", groups: ["ops", "employee"]},
    {userID: 3, name: "John", groups: ["qa", "employee"]},
    {userID: 4, name: "Paul", groups: ["dev", "qa", "employee"]}
];

var isDev = function (user) {
    return user.groups.includes("dev");
};

var isEmployee = function(user) {
    return user.groups.includes("employee");   
};

var isManager = function(user) {
    return user.groups.includes("manager");   
};

//every isDev
data.reduce(function(result, user) {
   return result && isDev(user);
}, true);  
//false, not everyone is a dev

//every isEmployee 
data.reduce(function(result, user) {
   return result && isEmployee(user);
}, true);
//true, everyone is an employee

//some isDev  
data.reduce(function(result, user) {
   return result || isDev(user);
}, false);  
//true, at least one user is a dev

//some isManager
data.reduce(function(result, user) {
   return result || isManager(user);
}, false);  
//false, no user is a manager
{% endhighlight %}

Now, do I recommend then that you just use `reduce` for everything and ignore the other built-in functions? Absolutely not - as you can see from the examples, the `reduce` versions are more complicated in every case.  Not bad - but definitely not as streamlined.  The API of the other functions help readability too - when you see `map` or `filter` you know exactly what is going on. Plus the specialized versions of these functions can take care of other optimizations behind the scenes.

Where `reduce` shines is when you either don't have a more specialized function to use, or when you might need to combine multiple actions together, like in our user / group combination example.

You should definitely learn `reduce` and how it works, as well as how to read it.  Get familiar with how the accumulation argument is passed from one iteration to the next - it's not difficult with very little practice.

Editorial Note: `reduce` can be called by many names in different languages.  `reduce` is by far the most common, but other languages might use `fold` or `aggregate`.  These are different words for the same concept.  There are also right and left versions of `reduce`, in JavaScript `reduce` is the left version.  Left and right just refer to if the reduction happens from left to right or right to left (ascending vs descending, forwards or backwards).  A right reduce is the same thing as doing a reverse of the data and then a left reduce.

## Notes

In _most_ languages, using these higher order functions instead of a loop is slower.  Almost always will be - the overhead of the function calls, plus the ability to use things like `break` or `continue` in certain examples means that you can optimize those loops easier.  But the speed comes at the cost of maintainability and readability.  In any language that provides these functions I will _always_ reach for these where I can and only begrudgingly go back and rewrite performance critical code into the loop version once testing shows it necessary.

You might notice I didn't talk about `forEach` - that is because while it is a higher order function, it doesn't generally take pure functions.  If you are passing a pure function to `forEach` you probably should be using `map` or something else. `forEach` (some languages just call it `each`) is for side effects - referencing outside variables (such as through closure) or writing output to the screen or talking to a database, etc.  There is nothing wrong with using it, but minimize it and consider first where you could use one of the other functions first and then use that output with your side-effecting code - it will provide much more testable and maintainable code.

## Conclusion

I hope these explanations and examples have whet your appetite and shown how you can do your everyday programming by passing around functions, leading to easier to read and test code. But, even though these are common software patterns, the goal shouldn't be to use them.  These are just tools that you should add to your repertoire and you should learn when they are and aren't appropriate.

That said, I believe that if you learn these patterns not only will you find ways to utilize them in your code, once you internalize the idea of first class functions and higher order functions you will start thinking of code very differently.  Be careful though, higher order functions are gateway drugs.  Soon you will be learing about currying, memoization and before you know it you're talking about monads, functors and tagging Hindley-Milner notation on train cars - I've seen it a thousand times. ;)

If you find any errors in this article, or have any other clarifications or insights to any of this, please leave a comment below, I would love to see them.

Update: Thanks to Dan L, Mingo Hagen, Paul Turner and Adam Cameron from the cfml-slack for proofreading :)
    

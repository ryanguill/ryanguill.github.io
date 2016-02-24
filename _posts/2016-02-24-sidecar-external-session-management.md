---
layout: post
title:  "Introducing Sidecar - external session management for ColdFusion"
date:   2016-02-24 12:00:00
author: Ryan Guill
categories: CFML
tags: CFML sessions redis sidecar
---


At [MotorsportReg](http://www.motorsportreg.com) we have customers all over the world so there is never a good time for maintenance or downtime. Historically, we used multiple application servers with sticky CFML sessions on the load balancer. Deploying code often meant interrupting users to deploy changes which is unacceptable. We needed more flexibility.

[Sidecar](https://github.com/MotorsportReg/sidecar) is our solution, an external session management plugin for ColdFusion.  Inspired by sessions in [expressjs](https://github.com/expressjs/session), we separated the persistence from the session management itself so you can plug in your favorite tech to fill that need - we wrote `redis_session_store.cfc` for our own needs, but all you have to do is implement the simple API for your preferred backend (memcached, couchdb, database, etc).  If you implement your own storage adapter, please [get in touch!](https://github.com/MotorsportReg/sidecar/issues)

Once you have the potential for multiple servers to access session data at the same time, you'll realize that `<cflock>` no longer offers the expected protection. We also wrote a separate distributed locking library, [cfml-redlock](https://github.com/MotorsportReg/cfml-redlock), to make concurrent access safer, [click here for some more info on that project](/cfml/2016/02/23/cfml-redlock.html)).

This software is used in production. We wanted to open source it so that others can benefit but, also, selfishly in the hope that other companies will test it, file issues, or contribute. Implementation is simple - take a look at the [tests](https://github.com/MotorsportReg/sidecar/tree/master/tests) and you should be able to get around pretty quickly. We plan to support Adobe ColdFusion 10+ and Lucee 4.5+ with this library.  

If you have a passion for speed or love cars, motorcycles or karts, check out [MotorsportReg](http://www.motorsportreg.com). We have more than 5,000 track days, autocross, races and tours you can get involved with - chances are there is something happening near you!

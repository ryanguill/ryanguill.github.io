---
layout: post
title:  "CFML-Redlock"
date:   2016-02-23 11:00:00
author: Ryan Guill
categories: CFML
tags: CFML sessions redis sidecar redlock
---


During the development of [Sidecar](https://github.com/MotorsportReg/sidecar), an external session management plugin for ColdFusion, we selected Redis as our storage backend to support sessions in a cluster. Without relying on sticky sessions, we quickly realized that we needed a way to ensure that we wouldn't step on our own toes as multiple servers potentially tried to access and modify session data concurrently.

After some research we decided on [redlock](http://redis.io/topics/distlock) for a distributed lock. This project is a port of  [node-redlock](https://github.com/mike-marcacci/node-redlock) to CFML. It is useful outside of session management for any scenario where multiple servers need to run a process with transaction semantics so we have released it as its own library. About the time we finished development, Ben Nadel released [his version of redlock](http://www.bennadel.com/blog/2945-cfredlock---my-coldfusion-implementation-of-the-redlock-distributed-locking-algorithm-from-redis.htm). They're similar but have a different API so check it out as well.

The goal is to support Adobe ColdFusion 10+ and Lucee 4.5+ with this library - like sidecar we are using these libraries in production, so we hope you find them useful and if welcome any contributions, including code, documentation or just reporting issues.

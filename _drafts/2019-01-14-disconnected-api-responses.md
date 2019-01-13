---
layout: post
title: "Disconnected API Responses"
date: 2019-01-14 12:00:00
author: Ryan Guill
categories: api rest queue
tags: api rest queue
cover:  "/assets/network-connection.jpg"
# original date 2017-10-26 12:00:00
---

An alternate title for this post might be `Processing API Requests with a Queue`. We recently had a project where we were expecting a burst of high traffic and heavy load on some API endpoints. We wanted to make sure that we could handle all of the traffic, even if the processing time was affected - dropped requests were not an option. After doing quite a bit of research this post is what we came up with. In the end this strategy worked well for our purposes, but we did identify some ways that we would improve it in the future.

Also this same strategy will work for any long-running api request. Things like reporting for example, where you need to be able to make a request but it may take a very long (and possibly indeterminate) amount of time to complete. Please forgive the tone of the document, it is being adapted from my notes and it isn't in conversational form. It's likely that there may be some things that I should expand upon, so if anything needs clarification please feel free to ask in the comments.

<!-- break -->

I am going to be talking both generically about the problem at a high level, but also specifically about the problem we were trying to solve. The goal with this work was to come up with a generic strategy, but obviously one that primarily fit our current needs.

For the purposes of this post let's define a bit of terminology and what is meant by these terms here:

- Client: program making an API call.
- Server: program receiving and responding to the API call.
- API: assume a REST API.
- Webhook: a url that the Server can call to deliver the result of the work requested.
- Response: the response from a given API call.
- Result: the ultimate result of the work requested.

Imagine three kinds of clients

- a browser which is able to take advantage of a websocket but not a webhook
- a server-like client that is able to receive a webhook and not a websocket.
- a script-like client that will make calls and may not be able to use a websocket or webhook.

All could take advantage of polling.

The use cases for this are several, but generally any long-running process that it isn't acceptable to have the client wait on a response, either from a server load perspective or a time-to-process perspective. Long running reports, server maintenance procedures, single-threaded operations under load.

We wanted something that could be applied to all client types to allow the server to process the requests in a queue and deliver results at a later time, disconnected from the original request.

For some applications that you control, a broadcast websocket channel may already be implemented for incremental updates to application state. But for some responses it might not be appropriate to broadcast to all clients on a websocket, either because the result is too large resulting in wasted bandwidth on the client side if clients are having to receive responses that do not apply for them, or the sensitivity of the result might not be appropriate for anyone other than the intended recipient. In these cases, the broadcast channel could be used to send a light-weight event to notify client of the completion of a request and then the source client can make a separate call to get the result instead of having to poll the server periodically.

Another option would be a separate websocket channel that could be created for each client and so the client could listen on that channel plus the broadcast channel. This is what we ended up doing for our needs - our client application created a unique websocket channel once it was logged in and that channel identifier was provided with each API request as where the response could be sent.

So here is the actual implementation we ended up with. There are two "status"es in play, the request status `PROCESSING|COMPLETE` and the result status that is context dependent and only exists once request status is `COMPLETE` e.g. `SUCCESS|ERROR`, `CREATED|INVALID_REQUEST|OVER_CAPACITY`

1. Client makes request to the API  
   Optionally provides a webhook url or websocket channel
   1. Server does a cursory validation of the request and
   inputs - returning a 404 for any missing/invalid inputs.
   2. Server generates requestID
   3. Server creates log record with:  
      requestID  
      requesting user  
      endpoint identifier (i.e. the rest endpoint)  
      `PROCESSING` request status  
      `NULL` result status  
      `NULL` result  
   4. Server adds request + requestID to queue
   5. Server responds with requestID and HTTP 202 / Accepted with a Content-Location header pointing to the endpoint where they can check the status of the request (see #4)  
   6. End of request.

2. Server processes queue
   1. Performs requested work
   2. Log for that requestID is updated to completed status and
   result of work
   3. If requested, Server calls webhook or notifies websocket  
      Server makes the determination to include entire result body over websocket based on size / sensitivity (determination decided per endpoint, not per request - this would be documented with the endpoint)

3. Client receives websocket message
   1. Filters to only request IDs that it is interested in, ignores others (in the case of a broadcast websocket channel - in our case the channel was private to the client so all messages were intended for this recipient.)
   2. If websocket message does not include response, based on the result status client calls API with request ID (see #4) (i.e. the status may be all the information necessary and the client doesn't need to go get the specific result)

4. Any client can call API to get current status of requestID  
   This is a generic endpoint, not related to the original endpoint called to make the initial request. For security, a client can only retrieve requests that it requested, based on authentication
   1. If not yet finished the status would still be PROCESSING with a 202 status code
      * It would be nice to be able to provide a progress indication here - at least for processes that lend themselves to having their progress measured  
   2. If finished, status would be `COMPLETE` with a 200 status code.  
      1. return the result status and the result of work (e.g. new order ID, error messages, report data, etc)  
      * The response could be cached once the result is complete.  

   * Note: this is the status of the Request not the Response - this endpoint may return a 200 saying the work is complete, even if the work had an error. The client needs  to check the Result to get the actual Response.  
   
   
   * If the result of the work was to create a new resource, a url/key to the created resource could be returned an then a 303 response might be more appropriate (see the link at the bottom of the post)  

Overall this scheme worked very well for us. It allowed us to have one server taking the requests serving the API but to use all of our servers as workers for the queue and responding to requests. One benefit is that scheme is agnostic to the result format, it could be JSON, CSV data, a link to another resource, etc. It also keeps your API server from being held open with long running requests.

Some other considerations that we did not implement but have thought about for the future:

Ideally you would want to implement some rate limiting on the polling endpoint and provide some guidance on how often it should be checked.

Because you need to log the result so that it is available for the client to pick up later, you need to think about how long you would commit to having the result available through the polling endpoint. You could imagine in a reporting scenario that the client may want to retrieve the results multiple times over time. You could implement an acknowledgement procedure along with an expiration time - possibly with a way to ask that the expiration be extended if that was necessary.

You may also want to provide the ability to cancel a request. Not all requests could be cancelled but that could be determined by endpoint.

The client could provide a key to sign the response and keep other clients from being able to read it, even if it was provided over a broadcast channel. This still has the same wasted-bandwidth problem for all but the smallest payloads though - and the encryption might make that problem worse.

We didn't come across this post until well after we were under-way but it has some very similar thoughts and expands in some different ways: [https://farazdagi.com/2014/rest-and-long-running-jobs/](https://farazdagi.com/2014/rest-and-long-running-jobs/)

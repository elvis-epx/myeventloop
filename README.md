# My Event Loop

This is a very simple, explicit and unambitious framework
for simple event-driven programs, e.g. TCP or UDP protocol
implementations.

It is a slightly improved version of some code I have been using
for many years to implement my own gimmicks. 

## Components

There are a couple examples ```(sample*.py)``` that are the best way to
know the framework and use as a starting point for your projects.

### myeventloop module

This module contains the base classes for all necessary components.

```MyEventLoop``` implements the event loop. It may be extended, but the
base class is concrete and usable by itself. 

```Handler``` is the abstract base class of a file descriptor handler.
The base class has no preconceptions about the kind of file descriptor it
will encapsulate.

```Timeout``` is the class that encapsulates a deferred task.

A Timeout may be owned by a Handler. This is handy when a connection closes
and the respective Handler is destroyed: all pending timeouts belonging
to the Handler are automatically cancelled.

```Log``` is a utility static class for logging. It can output messages
to terminal, to file and send by e-mail.

Since the implementation of event-driven TCP and UDP servers are the most
common use case, we provide extended classes for them:

### myeventloop/tcpserver submodule

```TCPServerEventLoop``` is extended with the typical plumbing
needed to set up a TCP server. You may still use the base class for
a TCP server if you prefer.

```TCPListener``` is a concrete extension of Handler that encapsulates a
TCP listening socket.

```TCPServerHandler``` is an abstract extension of Handler that encapsulates
an incoming TCP network connection. All non-blocking aspects of data
send/receive are implemented. You must extend this class and fill in 
your application protocol.

### myeventloop/tcpclient submodule

```TCPClientHandler``` is an abstract extension of Handler that encapsulates
an outgoing TCP network connection. All non-blocking aspects of data
send/receive are implemented, including non-blocking connection phase.
You must extend this class and fill in your application protocol.

### myeventloop/udpserver submodule

```UDPServerHandler``` is an abstract extension of Handler that encapsulates
a UDP network server.

Since UDP is connectionless, UDP servers and clients are very similar,
and a UDP protocol client handler may use this class as well. (The provided
UDP client example does exactly this.)

In this implementation, UDP is treated as connectionless. A single handler
exchanges packets from all remote peers, and no abstraction of a virtual
connection is implemented (nothing prevents implementing that on top of
it, though).

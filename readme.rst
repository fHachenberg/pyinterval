PyInterval Task/Event Logging Server
====================================

Mission
-------

Cycle duration is a critical variable for many iterative processes
like software development. The faster you can cycle, the faster you
can process new information or let your natural flow of thoughts
proceed. Slow cycles can limit efficiency because it stalls the flow
of thoughts and produces idle time. This idle time is often too small 
of a chunk to be usable for something else productively.

So we propably want to minimize our cycle time. How do we do it?
One very simple approach is to measure the time you spend on using
specific tools in your iteration cycle. Then we try to minimize this
time.

If you include all relevant tools in the cycle and assume that they
are executed sequentially, you end up with a time sum T. T represents
the optimal cycle duration currently achievable using your tools. 
  
For instance, a programmer will propably run her compiler and linker
(and possibly further targets in her build system) in every cycle 
and the necessary time for running these can very well (for larger 
projects) dominate the total cycle duration. 

pyinterval helps you to measure the time spent in specific tools by
offering you a simple client-server-application. The server runs 
locally on your machine and simply handles a sequence of events. The
client is meant to be used for instrumenting your tools. 

Instrumenting `make` via alias
------------------------------

    alias make='pyinterval_instrument "make $*"'

Evaluating the results
----------------------

TODO

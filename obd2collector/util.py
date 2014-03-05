#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#The MIT License (MIT)
#
#Copyright (c) 2013-2014 Christian Schwarz
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import threading
class Thread(threading.Thread):
    """Baseclass for all threads.

    It defines :py:meth:`shutdown()` to safely end the thread. In addition each
    instance has a :py:attr:`_lock` that can be used to safely lock critical
    sections.
    """

    ## a list containing all instances of Thread
    _runningThreads = []

    ## a classwide lock
    _lock = threading.Lock()

    @classmethod
    def shutdown_all(cls):
        """Shutsdown all running Threads."""
        cls._lock.acquire()

        runningThreads = filter(lambda t: t.isAlive(), cls._runningThreads)
    
        for t in runningThreads:
            t.shutdown()
            cls._runningThreads.remove(t)

        cls._lock.release()

    def __init__(self):
        """Initialized the Thread."""
        super(Thread, self).__init__()

        Thread._lock.acquire()
        Thread._runningThreads.append(self)
        Thread._lock.release()

        self._continueRunning = True
        self._lock            = threading.Lock()

    def shutdown(self):
        """Shuts down the Thread.

        This method call blocks until the Thread is finished.
        """
        self._continueRunning = False
        self.join()
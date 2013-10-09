#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#The MIT License (MIT)
#
#Copyright (c) 2013 Christian Schwarz
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

from configuration import CONFIGURATION

import threading

class LogServer(object):
	"""Serves the current logs via TCP/IP"""

	_ignoreLines = ["#GPS__", "#TIME__"]

	def __init__(self):
		"""Initializes the LogServer."""
		super(LogServer, self).__init__()

		self._port = CONFIGURATION["logServerPort"]

        self._currentData = []
		self._lock = threading.Lock()

	def add_entries(self, entries):
		"""Adds the given entries to the current log data.

		:param List entries:    List of log entries.
		"""
		for ignoreLine in LogServer._ignoreLines:
			entries = filter(lambda l: not l.startswith(ignoreLine), entries)

			if not entries:
				return

        self._lock.acquire()
        self._currentData += entries
        self._lock.release()

    def get_entries(self):
    	"""Returns all entries collected by the LogServer.

    	:warn:    All entires will be removed from the LogServers entries.

    	:return:    Returns a List containing all log entries.
    	:rtype:     List
    	"""
    	self._lock.acquire()
        entries = self._currentData
        self._currentData = []
        self._lock.release()

        return entries

from twisted.internet.protocol import Protocol
class LogSender(Protocol):
	"""The LogSender sends LogServer entries to the requesting client."""

	def dataReceived(self, data):
		"""
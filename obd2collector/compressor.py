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

from util import Thread
import time, subprocess

class Compressor(Thread):
    """The Compressor is used to compress the given log file."""

    def __init__(self):
        """Initialized the Compressor."""
        super(Compressor, self).__init__()

        self._filesToCompress = []

    def run(self):
        """Runs the Compressor."""
        while self._continueRunning:
            ## run only every 5 seconds.
            time.sleep(5)

            ## if no file needs to be compressed, compress its
            if len(self._filesToCompress) == 0:
                continue

            self._lock.acquire()
            filepath = self._filesToCompress[0]
            self._filesToCompress.remove(filepath)
            self._lock.release()

            self._compress_file(filepath)

        ## compress all remaining files
        self._lock.acquire()
        
        for f in self._filesToCompress:
            filepath = self._filesToCompress[0]
            self._filesToCompress.remove(filepath)
            self._compress_file(filepath)

        self._lock.release()

    def add_file_for_compression(self, filepath):
        """Adds a file for background compression.

        :param String filepath:    File that will be compressed (later).
        """
        self._lock.acquire()
        self._filesToCompress.append(filepath)
        self._lock.release()

    def _compress_file(self, filepath):
        """Compresses the given file.

        :param String filepath:    File that will be compressed (later).
        """
        subprocess.call(["gzip" , filepath])
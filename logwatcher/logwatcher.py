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

import threading, time

class LogWatcher(threading.Thread):
    """The LogWatcher looks periodically into a directory and reads the logs stored inside."""

    def __init__(self, dataPath):
        """Initializes the LogWatcher.

        :param String        dataPath:         Directory where the data will be stored.
        """
        super(LogWatcher, self).__init__()

        self.logEnding   = CONFIGURATION["logending"]
        
        self._dataPath    = dataPath
        self._newestFile  = None
        self._currentFile = None
        self._fileHandle  = None

        self._currentData = []

        self._lock = threading.Lock()
        
        self._watchLogs = True
        self.start()


    def shutdown(self):
        """Shuts down the LogWatcher."""
        self._watchLogs = False
        self.join()

    def check_for_new_logfile(self):
        """Checks, if a more current log file can be found."""

    def run(self):
        """Runs the LogWatcher."""

        ## open the nesest log file.
        self.check_for_new_logfile()
        self._fileHandle = file(self._newestFile, "rb")

        while self._watchLogs:
            ## sleep for 50ms
            time.sleep(0.05)

            ## open the new log file, if it exists.
            self.check_for_new_logfile()
            if self._currentFile != self._newestFile:
                self._currentFile.close()
                self._fileHandle = file(self._newestFile, "rb")
                self._currentFile = self._newestFile

            ## read all entries that are available right now
            self._lock.acquire()
            self._currentData.append(self._fileHandle.readlines())
            self._lock.release()

    def get_current_data(self):
        """Returns a dictionary containing the current LogData.

        :return:    Returns a list containing all data collected since the last call.
        :rtype:     List.
        """
        self._lock.acquire()
        result = self._currentData
        self._currentData = []
        self._lock.release()

        return self._currentData


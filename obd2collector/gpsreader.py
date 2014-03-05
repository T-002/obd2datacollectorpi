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

import gps, time

from util          import Thread
from configuration import CONFIGURATION

class GPSReader(Thread):
    """Class reading GPS reports created by gpsd."""

    def __init__(self):
        """Initializes the GPSReader."""
        super(GPSReader, self).__init__()
        
        ## read the GPS configuration
        self._gpsHost = CONFIGURATION["gpsdHost"]
        self._gpsdPort = CONFIGURATION["gpsdPort"]
        self.connect()
        
        ## initialize the report list
        self._gpsLogEntries = []
        
        ## start the thread
        self.start()
    
    def connect(self):
        """Connects to the GPS Daemon."""
        self._session = gps.gps(self._gpsHost, self._gpsdPort)
        self._session.stream(gps.WATCH_ENABLE | gps.WATCH_JSON)
    
    def _read_new_gps_entry(self):
        """Reads a new GPS entry from gpsd."""
        try:
            gpsEntry = self._session.next()
        except:
            self.connect()
            return
        
        self._lock.acquire()
        self._gpsLogEntries.append(gpsEntry)
        self._lock.release()
    
    def _get_and_clear_gps_log(self):
        """Gets all recorded GPS log entries."""
        self._lock.acquire()
        gpsLogEntries = self._gpsLogEntries
        self._gpsLogEntries = []
        self._lock.release()
        
        return [dict(gpsEntry) for gpsEntry in gpsLogEntries]
    
    def run(self):
        """Runs the GPS Reader until :py:meth:`GPSReader.shutdown` is called."""

        while self._continueRunning:
            self._read_new_gps_entry()
            time.sleep(0.5)
    
    def get_current_gps_entries(self):
        """Returns a list containin all collected GPS reports.

        :return:    Returns a list containing dictionaries which represent GPS reports.
        :rtype:     List
        """
        return self._get_and_clear_gps_log()

if __name__=="__main__":
    ## create a GPSReader instance
    gpsr = GPSReader()
    
    ## run for 30 seconds
    endTime = time.time() + 30
    while time.time() < endTime:
        print "%s\n" % "\n".join([str(e) for e in gpsr.get_current_gps_entries()])
        time.sleep(0.5)

    ## shut down the GPSReader
    gpsr.shutdown()
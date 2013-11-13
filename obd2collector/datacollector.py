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

import obd2reader
from gpsreader import GPSReader
from logserver import LogServer

from configuration import CONFIGURATION

from time import time as _getCurrentTime

class DataCollector(object):
    """The DataCollector collects and stores all data.

    The stored data includes:
        - Time
        - GPS data
        - OBD2 data
    """

    def __init__(self):
        """Initializes the DataCollector."""
        super(DataCollector, self).__init__()
        
        obd2readerClass  = getattr(obd2reader, CONFIGURATION["obd2reader"])
        self._obd2reader = obd2readerClass(CONFIGURATION["device"], CONFIGURATION["speed"])
        self._obd2reader.open_connection()

        self._gpsreader  = GPSReader(CONFIGURATION["gpsdPort"])

        self._logServer  = None
        if CONFIGURATION["logServer"]:
            self._logServer = LogServer()

    def shutdown(self):
        """Shuts down the DataCollector and all of its Threads."""
        self._obd2reader.shutdown()
        self._gpsreader.shutdown()

    def write_data_log(self, logFileName, nbrOfOBDFrames, messagesPerTimestamp):
        """Stores an data log file to the given location.

        :param String  logFileName:             Path to store the log file.
        :param Integer nbrOfOBDFrames:          Number of OBD frames to be stored inside the log.
                                                This parameter does NOT affect the number of time
                                                stamps or GPS reports.
        :param Integer messagesPerTimestamp:    Number of OBD2 frames share the same time stamp.

        :return:    Returns the number of bytes stored in the log.
        :rtype:     Integer
        """
        ## create the log file
        logf  = file(logFileName, "ab")
        
        ## performance optimization
        ## reduces the __getattr__ calls for the major instances
        write      = logf.write
        gpsreader  = self._gpsreader
        obd2reader = self._obd2reader
        logServer  = self._logServer

        ## number of bytes written
        bytes = 0

        ## collect the requested number of OBD2 frames
        for idx in xrange(0, nbrOfOBDFrames, messagesPerTimestamp):

            ## time stamp
            timestamp = "#TIME__%s\n" % _getCurrentTime()
            write(timestamp)

            ## send the timestamp to the logServer if requested            
            if logServer:
                logServer.add_entries([timestamp])

            bytes += len(timestamp)

            ## read the number of frames requested
            try:
                logEntries = obd2reader.read_frames(nbrOfOBDFrames)
            except:
                obd2reader.reconnect()
                continue

            ## send the log to the logServer if requested
            if logServer:
                logServer.add_entries(logEntries)
            
            ## store the frames in the log
            logEntries = "\n".join(logEntries)
            write("%s\n" % logEntries)
            bytes += len(logEntries) + 1

            ## append the gpslog entries, when there are any
            gpsreports = ["#GPS__%s\n" % entry for entry in gpsreader.get_current_gps_entries()]

            ## send the gps log to the logServer if requested
            if logServer:
                logServer.add_entries(gpsreports)
            
            ## no GPS report collected since last run
            if not gpsreports:
                continue

            ## store the reports in the log
            gpsreports = "\n".join([str(r) for r in gpsreports])
            write("%s\n" % gpsreports)
            bytes += len(gpsreports) + 1


        # close the log file
        logf.close()
        
        ## return the number of bytes written
        return bytes
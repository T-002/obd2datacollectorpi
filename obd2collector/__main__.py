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

## add the lib directory into the system path
import sys, os
sys.path.append("%s/lib" % os.path.dirname(os.path.realpath(__file__)))

from time          import time as _getCurrentTime
from display       import Display
from datacollector import DataCollector
from configuration import CONFIGURATION

def main(dataPath, datacollector, display):
    """Main function of the odb2collector.

    :param String        dataPath:         Directory where the data will be stored.
    :param DataCollector datacollector:    DataCollector instance used.
    :param Display       display:          Display instance used to show messages.
    """
    ## Numer of bytes stored
    loggedBytes = 0

    logEnding = CONFIGURATION["logending"]

    while True:

        message = [
            "Logged %skB" % (loggedBytes / 1024)
        ]
        
        print "\n".join(message)
        
        display.write_message(message)

        datafile = "%s/%s.%s" % (dataPath, _getCurrentTime(), logEnding)

        loggedBytes += datacollector.write_data_log(
            datafile,
            nbrOfOBDFrames=50000,
            messagesPerTimestamp=50
        )

if __name__=="__main__":

    ## make sure the script is called correctly
    if 2 != len(sys.argv):
        raise OSError("[ERROR] Correct usage:\n  python obd2collector <data directory>")

    dataPath      = sys.argv[1]
    datacollector = DataCollector()
    display       = Display()

    try:
        main(dataPath, datacollector, display)
    except KeyboardInterrupt:
        ## close all threads (hopefully)
        datacollector.shutdown()
        display.shutdown()
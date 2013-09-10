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

## add the lib dir into the python path, if the script is called directly
if __name__=="__main__":
    import os, sys
    sys.path.append("%s/lib" % os.path.dirname(os.path.realpath(__file__)))

from datetime         import datetime
from Adafruit_CharLCD import Adafruit_CharLCD
from configuration    import CONFIGURATION
import threading, time

## disable GPIO warnings
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

class Display(threading.Thread):
    """A wrapper class for the connected LC display."""
    
    def __init__(self):
        """Initializes the Display."""
        super(Display, self).__init__()
        
        self._lcd = Adafruit_CharLCD(pin_rs=CONFIGURATION["pin_rs"],
                                     pin_e=CONFIGURATION["pin_e"],
                                     pins_db=CONFIGURATION["pins_db"]
        )
        
        ## read the Display configuration
        self._width       = CONFIGURATION["width"]
        self._height      = CONFIGURATION["height"]
        self._refreshRate = CONFIGURATION["refreshRate"]
        
        self._lcd.begin(self._width, self._height-1)
        
        self._messages    = []
        
        self._lock = threading.Lock()
        
        ## start the Thread
        self._displayMessages = True
        self.start()
    
    def run(self):
        """Runs the Display thread until the Display is :py:meth:`Display.shutdown`."""
        while self._displayMessages:
            self._show_message()
            time.sleep(self._refreshRate)

    def shutdown(self):
        """Stops the Display and waits until it is shut down."""
        self._displayMessages = False
        self.join()
    
    def write_message(self, messages):
        """Writes the given messages onto the display.

        :param List messages:   A List of messages that will be displayed.
        """
        self._lock.acquire()
        self._messages = messages
        self._lock.release()
    
    def _show_message(self):
        """Displays the messages set by the last :py:meth:`Display.write_messages` call."""
        
        self._lock.acquire()
        self._lcd.clear()
        self._lcd.message(datetime.now().strftime("%b %d  %H:%M:%S\n"))
        for line in self._messages:
            self._lcd.message(line[:self._width])
        self._lock.release()

## makes the display script callable directly
if __name__=="__main__":
    ## initialize the display
    display = Display()
    
    ## read the script arguments and use them as messages
    messages = sys.argv
    print "\n".join(messages)
    
    ## set the messages and force the display to show it directly
    display.write_message(messages)
    display._show_message()

    ## shut down the spawned thread
    display.shutdown()
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

## disable GPIO warnings
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from Adafruit_CharLCD import Adafruit_CharLCD
class LCD(Adafruit_CharLCD):
    """Base class for all LCD instances."""

    def _get_screen_message(self, messages):
        """Returns a string, containing a writeable message for the display.
        
        :param List messages:    List of string containing the messages in their
                                 correct order.
        
        :return:    Returns a string that can be written onto the display.
        :rtype:     String
        
        :raise:     Raises a NotImplementedError if the derived class does not
                    overwrite the method.
        """
        raise NotImplementedError

    def _get_screen_message_list(self, messages):
        """Returns a list of display length fixed strings.

        :param List messages:    Messages to be modified.

        :return:    Returns a list, containing messages of the configured length.
        :rtype:     List
        """
        messages = messages[:self.numlines]
        messages = [message[:self.columns] for message in messages]

        messages = [message + " " * (self.columns - len(message)) for message in messages]
        
        while len(messages) < self.numlines:
            messages.append(" " * self.columns)

        return messages


class TwoLineLCD(LCD):
    """The TwoLineLCD can be used for two line HD44780 displays."""
    
    def _get_screen_message(self, messages):
        """Returns a string, containing a writeable message for the display.
        
        :param List messages:    List of string containing the messages in their
                                 correct order.
        
        :return:    Returns a string that can be written onto the display.
        :rtype:     String
        """
        return "".join(self._get_screen_message_list(messages))
        

class FourLineLCD(LCD):
    """The FourLineLCD can be used for four line HD44780 displays."""

    def _get_screen_message(self, messages):
        """Returns a string, containing a writeable message for the display.
        
        :param List messages:    List of string containing the messages in their
                                 correct order.
        
        :return:    Returns a string that can be written onto the display.
        :rtype:     String
        """
        messages = self._get_screen_message_list(messages)
        messages = [messages[0], messages[2], messages[1], messages[3]]
        return "".join(messages)
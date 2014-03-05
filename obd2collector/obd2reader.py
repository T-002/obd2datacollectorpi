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
class OBD2Reader(object):
    """Base class for all OBD2Reader.

    The OBD2Reader defines the methods that have to be implemented in the
    derived classes.
    """

    def __init__(self, device, speed, display=None):
        """Initializes the OBD2Reader.

        :param String  device:    OS path to the device used to collect the data.
        :param Integer speed:     Speed used to connect to the given device.
        :param Display display:   Display instance that can be used to view messages.
        """
        super(OBD2Reader, self).__init__()

        self._device  = device
        self._speed   = speed
        self._display = display

        self._wconnection   = None
        self._rconnection   = None
        self._connected     = False

    def shutdown(self):
        """Shuts down the OBD2Reader."""

    def open_connection(self):
        """Opens the connection to the given data collection device."""
        raise NotImplementedError

    def reconnect(self):
        """Reconnects the data reader."""
        raise NotImplementedError

    def send_command(self, command):
        """Sends the given command to the used adapter.

        :param String command:    Command that will be send.

        :return:    Returns if the command was send sucessfully or not.
        :rtype:     Boolean
        """
        raise NotImplementedError

    def read_frame(self):
        """Reads an OBD2 frame.

        :return:    Returns the OBD2 frame.
        :rtype:     String
        """
        raise NotImplementedError

    def read_frames(self, nbrOfFrames):
        """Returns a list containing the given number of OBD2 frames.

        :param Integer nbrOfFrames:    Number of OBD2 frames that should be read.

        :return:    Returns a list of OBD2 frames.
        :rtype:     List
        """
        return [self.read_frame() for idx in xrange(nbrOfFrames)]

import serial
class SerialDataReader(OBD2Reader):
    """An SerialDataReader used for OBD2 adapters connected via a serial interface, e.g. usbserial."""

    def open_connection(self):
        """Opens a new serial connection."""
        
        ## close already open connection
        if self._connected:
            self._rconnection.close()
            self._wconnection.close()
            self._rconnection = None
            self._wconnection = None

        self._rconnection = serial.Serial(self._device)
        self._wconnection = serial.Serial(self._device)

        crCount = 3
        self.send_command("\r" * crCount)
        
        ## set speed
        self.send_command(self._speed)

        ## disable timestamps
        self.send_command("Z0")
        
        ## open the can
        self.send_command("O")

    def reconnect(self):
        """Reconnects the data reader."""
        self.send_command("\r\rC\r%s\rO\r" % self._speed)

    def send_command(self, command):
        """Sends the given command to the adapter.

        :param String command:    Command that will be send.

        :return:    Returns if the command was send sucessfully or not.
        :rtype:     Boolean
        """
        res = self._wconnection.write("%s\r" % command)
        return res == (len(command) + 1)
        
    def read_frame(self):
        """Reads an OBD2 frame.

        :return:    Returns the OBD2 frame.
        :rtype:     String
        """
        read = self._rconnection.read
        
        ## read the first byte        
        frame = read()

        ## read the response identifier
        if "t"   == frame:
            frame += read(3)
        elif "T" == frame:
            frame += read(8)
        elif "\r" == frame:
            return frame
        else:
            rByte = read()
            while rByte != "\r":
                frame += rByte
                rByte = read()
 
            return frame
 
        ## read the data length
        dataBytes = read()
        frame += dataBytes
        
        ## read the data
        dataBytes = int(dataBytes)
        frame += read(2*dataBytes)
 
        ## read the final \\r
        end = read()
        if "\r" != end:
            frame = "#ERROR_MISSING_LINEBREAK__%s" % frame

        return frame

import bluetooth, time, sys
class BluetoothDataReader(OBD2Reader):
    
    def open_connection(self):
                ## close already open connection
        if self._connected:
            self._rconnection.close()
            self._wconnection.close()
            self._rconnection = None
            self._wconnection = None

        self._connection = self._get_connection()
        self.reconnect()

    def _get_connection(self):
        """Opens the RFCOMM connection.

        :return:    Returns the connection.
        :rtype:     bluetooth.BluetoothSocket.
        """
        socket = None
        print "Getting Connection..."

        retry = 0

        while not socket:
            try:
                print "Opening Socket"
                socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                socket.connect((self._device, 1))
            except bluetooth.btcommon.BluetoothError, e:
                socket = None
                time.sleep(1)
                
                message = e.message[1:-1].split(",")
                errorCode = int(message[0])
                
                ## something happened with the socket. A new socket should help
                if errorCode == 77:
                    continue

                ## Adapter cannot be found
                if errorCode == 112 or retry > 10:
                    self._display.write_message(["!Reconnect BTAdapter", "EC %s" % errorCode])
                    print "!Reconnect BTAdapter"
                    time.sleep(5)
                    continue

                ## Adapter is in error state
                if errorCode in [113, 115, 52]:
                    self._display.write_message(["!Reset BTAdapter", "EC %s" % errorCode])
                    print "!Reset BTAdapter %s" % errorCode
                    time.sleep(5)
                    retry = 0
                    continue

                ## Device is busy, we should wait a little longer
                if errorCode == 16:
                    self._display.write_message(["Waiting for BTAdapter", "EC %s" % errorCode])
                    print "Waiting for BTAdapter"
                    retry += 1
                    continue


                self._display.write_message(["Unknown Error", "EC %s" % errorCode])
                print "Unknown Error"
                print e
                sys.exit()
    
        self._display.write_message(["BT Connection OK"])
        print "BT Connection OK"
        return socket
    
    def reconnect(self):
        self.send_command("Z")
        self.read_frame()
        self.read_frame()
        self.read_frame()
        
        self.send_command("AL")
        self.read_frame()
        self.read_frame()
        self.read_frame()
        
        #self.send_command("L1")
        #self.read_frame()
        #self.read_frame()
        #self.read_frame()
        
        self.send_command("H1")
        self.read_frame()
        self.read_frame()
        self.read_frame()
        
        self.send_command("S1")
        self.read_frame()
        self.read_frame()
        self.read_frame()

        self.send_command("CAF0")
        self.read_frame()
        self.read_frame()
        self.read_frame()

        self.send_command("D1")
        self.read_frame()
        self.read_frame()
        self.read_frame()
        
        self.send_command("MA")
        self.read_frame()
        self.read_frame()
        self.read_frame()
            
    def send_command(self, command, prefixAT=True):
        """Sends the given command to the adapter.

        :param String command:    Command that will be send.
        :param Bool   prefixAT:   Automatically adds the 'AT' to the command.

        :return:    Returns if the command was send sucessfully or not.
        :rtype:     Boolean
        """
        if prefixAT:
            command = "AT%s" % command
        
        res = self._connection.send("%s\r" % command)
        return res == (len(command)) + 1
    
    def read_frame(self):
        result = ""
        data = self._connection.recv(1)
        while data != "\r":
            result += data
            data = self._connection.recv(1)

        if "BUFFER FULL" in result:
            #print "\n"
            self.send_command("BD")
            self.send_command("MA")
            return self.read_frame()
        
        return result
    
def main():
    from display import Display

    display = Display()
    
    #reader = BluetoothDataReader("00:04:3E:26:08:CB", 1, display)
    reader = BluetoothDataReader("/dev/rfcomm99", 1, display)

    reader.open_connection()
    
    while True:
        res = reader.read_frame()
        
        if res == "\n":
            continue
        
        print res
        continue
    
        cmd = raw_input("Command: ")
        
        if cmd != "read":
            if not reader.send_command(cmd):
                print "Could not send command %s" % cmd
                continue
        
        print reader.read_frame()

if __name__=="__main__":
    try:
        main()
    except:
        sys.exit(0)
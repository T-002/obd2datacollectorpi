#!/bin/bash
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

# change to working directory
cd $WORKDIR

## create log
echo "#######################"                                     >  $LOG
echo "# OBD2 data collector #"                                     >> $LOG
echo "#######################"                                     >> $LOG

## change into working directory
echo "[`date`] Changed already into working directory. ("$WORKDIR")" >> $LOG

## check for usb mount
#echo "[`date`] Checking for USB stick availablility"                 >> $LOG
#while [ ! -e $USBSTICK ]
#do
#    echo "[`date`]  [ERROR] USB Stick not found... ($USBSTICK)"
#    echo "[`date`]  [ERROR] USB Stick not found... ($USBSTICK)"      >> $LOG
#    python obd2collector/display.py "E: USB missing."
#    sleep 3
#done

if [ ! -d data ] ; then
    echo "[`date`]  [WARNING] data directory not found."             >> $LOG
    mkdir data                                                       >> $LOG
fi

STICKMOUNTED=`cat /etc/mtab | grep $USBSTICK | wc -l`
if [ $STICKMOUNTED -ne 1 ] ; then
    echo "[`date`] Mounting USB stick ($WORKDIR/data)"               >> $LOG
    mount $USBSTICK $WORKDIR/data                                    >> $LOG 2>> $LOG
fi

# restarting bluetooth
echo "[`date`] Restarting Bluetooth"                                 >> $LOG 2>> $LOG
/etc/init.d/bluetooth restart

## check for adapter
#echo "[`date`] Looking for CAN adapter"                              >> $LOG
#while [ ! -e $CANADAPTER ]
#do
#    echo "[`date`]  [ERROR] CAN adapter not found... ($CANADAPTER)"
#    echo "[`date`]  [ERROR] CAN adapter not found... ($CANADAPTER)"  >> $LOG
#    python obd2collector/display.py "E: CAN missing."
#    sleep 3
#done

# create directory
echo "[`date`] Creating data directory"                              >> $LOG 2>> $LOG
mkdir -p $DATADIR

# call collector
echo "[`date`] Starting data collection"                             >> $LOG
python obd2collector/display.py "Running..."
python -u obd2collector $DATADIR                                     >> $LOG 2>> $LOG
   
## change back into starting directory
echo "[`date`] Done."                                                >> $LOG

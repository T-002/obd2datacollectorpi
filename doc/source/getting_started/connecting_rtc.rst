.. index

Connecting a Real Time Clock to your Raspberry
==============================================

The Raspberry Pi does not have a clock that is running, even if the Raspberry Pi itself is switched off.
The installed software solution of using ntp for initial setup and persiting the time periocally works good for the majority of the Raspberry Pi use cases, having the Raspberry conntected to the internet.

The OBD2 data collector will be installed inside a vehicle, having no internet connection to synchronize the time.
Therefore the Raspberry Pi will be equipped with a hardware clock module.

The install instructions are mainly for the `RasClock <http://afterthoughtsoftware.com/products/rasclock>`_.


Installing the Clock
--------------------
To install the clock, please wire the 3.3V, GND, SDA and SCL pin to the Raspberry Pi.


Installing the RTC Kernel
-------------------------

change into root shell


install the kernel
    wget http://afterthoughtsoftware.com/files/linux-image-3.6.11-atsw-rtc_1.0_armhf.deb
    dpkg -i linux-image-3.6.11-atsw-rtc_1.0_armhf.deb
    mv /boot/kernel.img /boot/kernel.img.old
    cp /boot/vmlinuz-3.6.11-atsw-rtc+ /boot/kernel.img
    rm linux-image-3.6.11-atsw-rtc_1.0_armhf.deb

add the required modules:
    echo "i2c-bcm2708"  >> /etc/modules
    echo "rtc-pcf2127a" >> /etc/modules

enable RTC at boot time (edit /etc/rc.local)
    echo pcf2127a 0x51 > /sys/class/i2c-adapter/i2c-1/new_device
    ( sleep 2; hwclock -s ) &

reboot the system
    reboot

remove fake rtc
    apt-get remove fake-hwclock
    rm /etc/cron.hourly/fake-hwclock
    update-rc.d -f fake-hwclock remove
    rm /etc/init.d/fake-hwclock


persist ntp datetime to hwclock automatically
    echo '#!/bin/bash'  > /etc/cron.daily/hwclock-sync 
    echo 'hwclock -w' >> /etc/cron.daily/hwclock-sync
    chmod a+x /etc/cron.daily/hwclock-sync



Additional Information
----------------------
For more information, please take a look into the `original instructions <http://afterthoughtsoftware.com/products/rasclock>`_.
* :ref:`search`
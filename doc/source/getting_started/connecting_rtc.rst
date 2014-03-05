.. index

Connecting a Real Time Clock
============================

The Raspberry Pi does not have a clock that is running, even if the Raspberry Pi itself is switched off.
The installed software solution of using ntp for initial setup and persiting the time periocally works good for the majority of the Raspberry Pi use cases, having the Raspberry conntected to the internet.

The OBD2 data collector will be installed inside a vehicle, having no internet connection to synchronize the time.
Therefore the Raspberry Pi will be equipped with a hardware clock module.

The install instructions are mainly for the `RasClock <http://afterthoughtsoftware.com/products/rasclock>`_.


Hardware Installation
---------------------
To install the clock, please wire the 3.3V, GND, SDA and SCL pin to the Raspberry Pi.


Software Installation
---------------------

You should change into a root shell::

    sudo -i

Install a linux kernel with real time clock support (`RasClock <http://afterthoughtsoftware.com/products/rasclock>`_ in our case)::

    wget http://afterthoughtsoftware.com/files/linux-image-3.6.11-atsw-rtc_1.0_armhf.deb
    dpkg -i linux-image-3.6.11-atsw-rtc_1.0_armhf.deb
    mv /boot/kernel.img /boot/kernel.img.old
    cp /boot/vmlinuz-3.6.11-atsw-rtc+ /boot/kernel.img
    rm linux-image-3.6.11-atsw-rtc_1.0_armhf.deb

You need to add the required modules at boot time.::

    echo "i2c-bcm2708"  >> /etc/modules
    echo "rtc-pcf2127a" >> /etc/modules

Add the following two lines to ``/etc/rc.local``, just before the ``exit 0`` at the end.::

    echo pcf2127a 0x51 > /sys/class/i2c-adapter/i2c-1/new_device
    ( sleep 2; hwclock -s ) &

Finally! :)::

    reboot

Optional Steps
--------------
After installing the RTC, you should be able to remove the ``fake-hwclock``.::

    apt-get -y remove fake-hwclock
    rm /etc/cron.hourly/fake-hwclock
    update-rc.d -f fake-hwclock remove
    rm /etc/init.d/fake-hwclock

To periodically write back the system clock to the RTC, in case of periodically NTP synchronization, you can do the following.::

    echo '#!/bin/bash'  > /etc/cron.daily/hwclock-sync 
    echo 'hwclock -w' >> /etc/cron.daily/hwclock-sync
    chmod a+x /etc/cron.daily/hwclock-sync


References
----------
 * `Original RasClock Instructions <http://afterthoughtsoftware.com/products/rasclock>`_
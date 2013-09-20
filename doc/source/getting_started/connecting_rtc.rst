.. index

Connecting a Real Time Clock to your Raspberry
==============================================


http://afterthoughtsoftware.com/products/rasclock

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
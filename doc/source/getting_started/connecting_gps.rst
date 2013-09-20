.. index

http://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/setting-everything-up


sudo apt-get install gpsd gpsd-clients python-gps


sudo update-rc.d gpsd defaults


sudo nano /boot/cmdline.txt
change to
    dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p6 rootfstype=ext4 elevator=deadline rootwait

sudo nano /etc/inittab
change to
    #T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100

sudo nano /etc/default/gpsd
change to
    START_DAEMON="true"
    DEVICES="/dev/ttyAMA0"


reboot


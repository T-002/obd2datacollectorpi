.. index

Connecting Pif 7000
===================

Preparing Raspberry
-------------------
nano /etc/modprobe.d/raspi-blacklist.conf
    #blacklist spi-bcm2708
    #blacklist i2c-bcm2708

nano /etc/modules
    i2c-bcm2708
    i2c-dev

reboot

i2cdetect -y 1



Installing Bugblat Software
---------------------------
cd /opt/pif/software/src

make & make install

cd .. && python piffind.py


Installing MyHDL
----------------
wget http://downloads.sourceforge.net/project/myhdl/myhdl/0.8/myhdl-0.8.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fmyhdl%2Ffiles%2Fmyhdl%2F&ts=1384361168&use_mirror=netcologne

mv myhdl-0.8.tar.gz\?r\=http\:%2F%2Fsourceforge.net%2Fprojects%2Fmyhdl%2Ffiles%2Fmyhdl%2F myhdl-0.8.tar.gz

tar xvf myhdl-0.8.tar.gz

cd myhdl-0.8

python setup.py install

cd myhdl/test/core

python test_all.py
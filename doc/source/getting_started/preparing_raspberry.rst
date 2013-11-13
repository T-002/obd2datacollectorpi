.. index

Preparing the Raspberry Pi
--------------------------

Update all packages
    apt-get update
    apt-get upgrade
    apt-get autoremove

Install helpful tools
    apt-get -y install screen python-setuptools locate python-sphinx python-coverage python-twisted python-smbus i2c-tools python-webpy

Cloning repositories
    git clone https://github.com/T-002/obd2datacollectorpi.git /opt/obd2datacollectorpi
    git clone https://github.com/bugblat/pif.git /opt/pif



Installing Bluetooth (installs a lot of dependencies)
    apt-get install bluetooth

    update-rc.d bluetooth defaults
    hciconfig -a

    http://www.raspberrypi.org/phpBB3/viewtopic.php?t=9585&p=276881




Disable IPv6 (optional)
    echo "install ipv6 /bin/true" >> /etc/modprobe.d/blacklist.conf

Install Adafruit WebIDE (optional)
    curl https://raw.github.com/adafruit/Adafruit-WebIDE/alpha/scripts/install.sh | sudo sh
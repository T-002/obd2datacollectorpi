.. index

Preparing the Raspberry Pi
--------------------------

Update all packages
    apt-get update
    apt-get upgrade
    apt-get autoremove

Install helpful tools
    apt-get -y install screen python-setuptools locate python-sphinx python-coverage

Cloning repository
    git clone https://github.com/T-002/obd2datacollectorpi.git /opt/obd2datacollectorpi






Disable IPv6 (optional)
    echo "install ipv6 /bin/true" >> /etc/modprobe.d/blacklist.conf

Install Adafruit WebIDE (optional)
    curl https://raw.github.com/adafruit/Adafruit-WebIDE/alpha/scripts/install.sh | sudo sh
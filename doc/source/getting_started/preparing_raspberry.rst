.. index

Preparing the Raspberry Pi
--------------------------

Update all packages
apt-get update
apt-get upgrade


Disable IPv6 (optional)
echo "install ipv6 /bin/true" >> /etc/modprobe.d/blacklist.conf

Install Adafruit WebIDE (optional)
curl https://raw.github.com/adafruit/Adafruit-WebIDE/alpha/scripts/install.sh | sudo sh
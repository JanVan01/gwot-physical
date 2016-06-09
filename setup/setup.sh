#!/bin/sh

# Install needed packages from apt-get
apt-get install python3
apt-get install python3-pip
apt-get install python3-rpi.gpio
apt-get install mosquitto
apt-get install postgresql-9.4-postgis-2.1
apt-get install postgresql-server-dev-9.4


# Download dependencies from pip3
pip3 install apidoc

# Create database etc

# Set CHMOD
chmod 755 ../*.py

# Create cron job?

# Install as a service
cp ./etc/init.d/gwot-server /etc/init.d/
chmod 755 /etc/init.d/gwot-server
update-rc.d /etc/init.d/gwot-server defaults
/etc/init.d/gwot-server start

# Create API-DOC?
apidoc -i ./dev/apidoc.yml -o ../static/apidoc/index.html
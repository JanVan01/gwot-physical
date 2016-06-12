#!/bin/sh

# Check arguments
if [ $# != 2 ]
	then echo "Please specify these two parameters: 1. database name, 2. database password" && exit
fi

# Set current working directory to folder of this file
cd "$(dirname "$0")"

# Set some commonly used variables
HOST=hostname
DBNAME=$1
DBPASSWORD=$2

# Add mosquitto repository
# wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
# apt-key add mosquitto-repo.gpg.key
# wget http://repo.mosquitto.org/debian/mosquitto-wheezy.list -P /etc/apt/sources.list.d/

# Install needed packages from apt-get
apt-get update
apt-get install -y python3
apt-get install -y python3-pip
apt-get install -y python3-rpi.gpio
apt-get install -y mosquitto
apt-get install -y postgresql-9.4-postgis-2.1
apt-get install -y postgresql-server-dev-9.4

# Download dependencies from pip3
pip3 install -r ../requirements.txt

# Write config.ini
cat <<EOF > ../data/config.ini
[Config]
name = $HOST
location = 0
interval = 30
password = admin
dbhost = localhost
dbuser = postgres
dbpw = $DBPASSWORD
dbname = $DBNAME

[Default]
name = $HOST
location = 0
interval = 30
password = admin
dbhost = localhost
dbuser = postgres
dbpw = $DBPASSWORD
dbname = $DBNAME
EOF

# Database setup
sudo -u postgres psql -c"CREATE DATABASE $DBNAME;"
sudo -u postgres psql -X -f schema.sql --echo-all --set AUTOCOMMIT=on --set ON_ERROR_STOP=on $DBNAME
if [ $? != 0 ]; then
    echo "Could not execute schema.sql, please run it manually on psql." 1>&2
fi
sudo -u postgres psql -c"ALTER user postgres WITH PASSWORD '$DBPASSWORD'"
/etc/init.d/postgresql restart

# Set CHMOD to allow main py files to be executable
chmod 755 ../*.py

# Create cron job
crontab -l > crontab.tmp
echo "* * * * * /home/pi/gwot-physical/scheduler.py" >> crontab.tmp
crontab crontab.tmp
rm crontab.tmp

# Install as a service
cp ./etc/init.d/gwot-server /etc/init.d/
chmod 755 /etc/init.d/gwot-server
update-rc.d /etc/init.d/gwot-server defaults
/etc/init.d/gwot-server start

# Create API-DOC
apidoc -i ./dev/apidoc.yml -o ../static/apidoc/index.html
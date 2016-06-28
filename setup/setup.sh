#!/bin/sh

# Check arguments
if [ $# != 2 ]
	then echo "Please specify these two parameters: 1. database name, 2. database password" && exit
fi

echo "#################################################"
echo "###                SETUP STARTED"
echo "###"
HOST=$(hostname)
echo "### Hostname: $HOST"
DBNAME=$1
echo "### DB name: $DBNAME"
DBPASSWORD=$2
echo "### DB password: $DBPASSWORD"
SETUPDIR=$(cd $(dirname "$0"); pwd)
echo "### Setup directory: $SETUPDIR"
APPDIR=$(dirname "$SETUPDIR")
echo "### App directory: $APPDIR"
echo "#################################################"

# Set current working directory to folder of this file
cd "$SETUPDIR"

# Install needed packages from apt-get
apt-get update
apt-get install -y perl
apt-get install -y python3
apt-get install -y python3-pip
apt-get install -y python3-rpi.gpio
apt-get install -y mosquitto
apt-get install -y postgresql-9.4-postgis-2.1
apt-get install -y postgresql-server-dev-9.4

# Download dependencies from pip3
pip3 install -r ../requirements.txt

# Rename sample config.ini
cp ../data/config.ini.sample ../data/config.ini

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
sudo -u postgres psql -X -f dev/schema.sql --echo-all --set AUTOCOMMIT=on --set ON_ERROR_STOP=on $DBNAME
if [ $? != 0 ]; then
    echo "Could not execute $SETUPDIR/dev/schema.sql, please run it manually on psql." 1>&2
fi
sudo -u postgres psql -c"ALTER user postgres WITH PASSWORD '$DBPASSWORD'"
/etc/init.d/postgresql restart

# Set CHMOD to allow main py files to be executable
chmod 755 ../*.py

# Create cron job
crontab -l > crontab.tmp
echo "* * * * * $APPDIR/scheduler.py" >> crontab.tmp
crontab crontab.tmp
rm crontab.tmp

# Install as a service
perl -pi -e "s:#__Set your program directory here__:$APPDIR:g" dev/gwot-server
cp dev/gwot-server /etc/init.d/
chmod 755 /etc/init.d/gwot-server
update-rc.d gwot-server defaults
/etc/init.d/gwot-server start

# Create API-DOC
apidoc -i ./dev/apidoc.yml -o ../static/apidoc/index.html

echo "\n\n\n\n\n\n"
echo "#################################################"
echo "###                SETUP FINISHED"
echo "###"
echo "### Visit the following URL to access the server:"
echo "### http://$HOST:5000"
echo "#################################################"

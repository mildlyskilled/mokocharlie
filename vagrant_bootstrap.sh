#!/usr/bin/env bash
!/bin/sh
clear
echo "\n--- Ladies and Gentlemen, hold on to your shirts ---"
echo "\n--- we're building Mokocharlie  dev box... ---"

DBHOST=localhost
DBNAME=moko
DBUSER=root
DBPASSWD=root

echo "\n--- Updating packages list ---\n"
apt-get update
apt-get -y autoremove
apt-get -y autoclean

cd /home/vagrant
mkdir -p /home/vagrant/log

echo "\n--- Setting up MySQL Credentials ---\n"
echo "mysql-server mysql-server/root_password password $DBPASSWD" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password $DBPASSWD" | debconf-set-selections

apt-get install -y python-pip python-dev zlib1g-dev libpng12-dev libjpeg-dev language-pack-en mysql-client-core-5.5 mysql-server-5.5 libmysqlclient-dev python-mysqldb screen libpq-dev
echo "\n- Symlinking some important stuff for image processing -\n"
ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
echo "\n------------------ Done Symlinking ---------------------\n"

echo "\n--- Create database --\n"
mysql -uroot -p$DBPASSWD -e "CREATE DATABASE IF NOT EXISTS $DBNAME;"
mysql -uroot -p$DBPASSWD -e "GRANT ALL PRIVILEGES ON $DBNAME.* TO '$DBUSER'@'localhost' IDENTIFIED BY '$DBPASSWD';"
mysql -uroot -p$DBPASSWD -e "FLUSH PRIVILEGES;"

mysql -u$DBUSER -p$DBPASSWD $DBNAME < /home/vagrant/mokocharlie/data/moko.sql

pip install -r /home/vagrant/mokocharlie/requirements.txt
cd /home/vagrant/mokocharlie
python manage.py syncdb --settings=moko.settings.dev
mysql -u$DBUSER -p$DBPASSWD $DBNAME < /home/vagrant/mokocharlie/data/0001_inserts.sql
mysql -u$DBUSER -p$DBPASSWD $DBNAME < /home/vagrant/mokocharlie/data/0002_m2m.sql
mysql -u$DBUSER -p$DBPASSWD $DBNAME < /home/vagrant/mokocharlie/data/0003_drops.sql
python manage.py migrate --fake-initial --settings=moko.settings.dev

echo "\n------ PROVISIONING COMPLETE RUN PYTHON MANAGE ------"
echo "\n-----------------------------------"



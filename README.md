MIGRATING DATA FOR NEW PLATFORM
============================================

* Import from data dump
* Run data/up.sql (takes a while)
* If migrations folder exists in common rename or delete it
* Run ./manage.py syncdb
* Run data/up2.sql
* Run ./manage.py schemamigration common --initial
* Run ./manage.py migrate common 0001 --fake
* Run ./manage.py migrate common

Foreman
-----------
This project also has a Procfile for a foreman deploy
MIGRATING DATA FOR NEW PLATFORM
============================================

* Import from data dump
* If migrations folder exists in common rename or delete it
* Run ./manage.py syncdb
* Run data/0001_inserts.sql
* Run data/0002_m2m.sql
* Run data/0003_drops.sql
* Run ./manage.py schemamigration common --initial
* Run ./manage.py migrate common 0001 --fake
* Run ./manage.py migrate common

Foreman
-----------
This project also has a Procfile for a foreman deploy
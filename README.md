MIGRATING DATA FOR NEW PLATFORM
============================================

* Import from data dump
* If migrations folder exists in common rename or delete it
* Import data/moko.sql
* Run ./manage.py syncdb
* Run data/0001_inserts.sql
* Run data/0002_m2m.sql
* Run data/0003_drops.sql
* Run ./manage.py migrate --fake-initial

Foreman
-----------
This project also has a Procfile for a foreman deploy
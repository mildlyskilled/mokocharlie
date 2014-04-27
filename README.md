MIGRATING DATA FOR NEW PLATFORM
============================================

* Import from data dump
* Run data/up.sql (takes a while)
* Run ./manage.py syncdb
* Run data/up2.sql
* Run ./manage.py migrate common 0001 --fake
* Run ./manage.py migrate common

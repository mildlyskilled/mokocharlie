MIGRATING DATA FOR NEW PLATFORM
============================================

* Import from data dump
* Run data/up.sql (takes a while)
* Run ./manage.py syncdb
* Run data/up2.sql
* Run data/up3.sql
* Run ./manage.py schemamigration --initial
* Run ./manage.py migrate common --fake

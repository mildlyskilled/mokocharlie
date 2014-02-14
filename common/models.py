from __future__ import unicode_literals
from django.db import models


class Taxonomy(models.Model):
    tax_id = models.BigIntegerField(primary_key=True)
    tax_name = models.CharField(max_length=25)
    tax_description = models.TextField()
    tax_class = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'taxonomy'


class Log(models.Model):
    log_id = models.IntegerField(primary_key=True)
    log_type = models.IntegerField()
    log_no = models.CharField(max_length=4)
    log_description = models.TextField()
    log_source = models.CharField(max_length=150)
    log_date = models.DateTimeField()
    log_assignee = models.CharField(max_length=41)

    class Meta:
        managed = False
        db_table = 'moko_log_data'

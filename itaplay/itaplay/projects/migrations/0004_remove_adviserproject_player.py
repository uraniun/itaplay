# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-05 07:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_adviserproject_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adviserproject',
            name='player',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-15 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_auto_20160815_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='player_status',
            field=models.BooleanField(default=False),
        ),
    ]

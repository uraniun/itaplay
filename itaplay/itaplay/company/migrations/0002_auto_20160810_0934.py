# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-10 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='administrator',
            field=models.IntegerField(default=1),
        ),
    ]

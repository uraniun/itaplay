# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-11 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clips', '0002_remove_clip_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='clip',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-02 07:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_sound_nano_time_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sound',
            name='nano_time_start',
        ),
    ]

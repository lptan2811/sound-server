# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-02 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20180326_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='sound',
            name='nano_time_start',
            field=models.IntegerField(null=True),
        ),
    ]

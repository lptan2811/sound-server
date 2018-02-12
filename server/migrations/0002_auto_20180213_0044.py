# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-12 17:44
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sound',
            name='sr',
            field=models.IntegerField(default=16000),
        ),
        migrations.AddField(
            model_name='sound',
            name='time_start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='sound',
            name='wave',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, default=[], size=None),
        ),
        migrations.AlterField(
            model_name='sound',
            name='label',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True),
        ),
    ]
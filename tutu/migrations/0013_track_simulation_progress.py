# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutu', '0012_auto_20170724_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='simulation_progress',
            field=models.BooleanField(default=False),
        ),
    ]
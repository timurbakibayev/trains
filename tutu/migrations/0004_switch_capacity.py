# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutu', '0003_auto_20170722_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='capacity',
            field=models.IntegerField(default=1),
        ),
    ]
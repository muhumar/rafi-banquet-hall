# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-21 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realapp', '0003_auto_20180220_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='additional_overall_cost',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-20 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realapp', '0002_event_conclude_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='additional_cost_perhead',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]

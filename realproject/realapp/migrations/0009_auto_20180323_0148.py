# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-23 08:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('realapp', '0008_event_special_arrangement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event_special_arrangement',
            old_name='arrange_id',
            new_name='special_arrange_id',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-09 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realapp', '0013_print'),
    ]

    operations = [
        migrations.AddField(
            model_name='print',
            name='print_details',
            field=models.CharField(default='', max_length=50),
        ),
    ]
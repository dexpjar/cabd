# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-17 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180317_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='paramsinput',
            name='value',
            field=models.CharField(default='', max_length=100, verbose_name='Value'),
            preserve_default=False,
        ),
    ]

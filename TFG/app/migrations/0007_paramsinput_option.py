# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-17 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_paramsinput_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='paramsinput',
            name='option',
            field=models.CharField(default='', max_length=100, verbose_name='Option'),
            preserve_default=False,
        ),
    ]

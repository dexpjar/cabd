# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-17 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_paramsinput_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paramsinput',
            name='state',
            field=models.CharField(choices=[('text', 'Text'), ('file', 'File'), ('read', 'Read')], default='text', max_length=15),
        ),
    ]

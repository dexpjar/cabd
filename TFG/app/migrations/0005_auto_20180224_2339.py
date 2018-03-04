# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-24 23:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180224_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParamsInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('state', models.CharField(choices=[('text', 'Text'), ('file', 'File')], default='text', max_length=15)),
                ('allowed_format', models.CharField(max_length=100, verbose_name='Allowed Format')),
            ],
        ),
        migrations.CreateModel(
            name='Taks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('state', models.CharField(choices=[('pending', 'Pending'), ('in_queue', 'In Queue'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=15)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('file_input', models.FileField(upload_to='files/input/', verbose_name='File Input')),
                ('file_output', models.FileField(blank=True, upload_to='files/output/', verbose_name='File Output')),
            ],
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.AlterModelOptions(
            name='app',
            options={},
        ),
        migrations.AddField(
            model_name='taks',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='app.App'),
        ),
    ]

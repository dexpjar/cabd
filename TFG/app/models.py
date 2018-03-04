# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Section(models.Model):
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Section')
    subsection = models.ForeignKey('self')

class ParamsInput(models.Model):
    LIST_INPUT = (
    ('text', 'Text'), ('file', 'File'))

    name = models.CharField('Name', max_length=100)
    state = models.CharField(
        max_length=15,
        choices=LIST_INPUT,
        default='text',
    )
    allowed_format = models.CharField('Allowed Format', max_length=100)

def image_upload_location(instance, filename):
    return 'app/%s.png' % (instance.id)

class App(models.Model):
    taskcode = models.CharField('TaskCode', max_length=100)
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    citation = models.TextField('Citation')
    image = models.ImageField('Image', blank=True, null=True, upload_to=image_upload_location)
    # class Meta:
    #     verbose_name = 'App'
    #     verbose_name_plural = 'Apps'
    #     ordering = ['name']
    #
    def __str__(self):
        return '{}'.format(self.name)



class Task(models.Model):
    LIST_STATES = (('pending','Pending'),('in_queue','In Queue'),('completed','Completed'),('canceled','Canceled'))

    name = models.CharField('Name', max_length=100)
    state = models.CharField(
        max_length=15,
        choices=LIST_STATES,
        default='pending',
    )
    app = models.ForeignKey(App, related_name="application")
    user = models.ForeignKey(User, related_name="user")
    creation_date = models.DateTimeField('Creation Date',auto_now_add=True)
    file_input = models.FileField('File Input', upload_to='files/input/',blank=False)
    file_output = models.FileField('File Output', upload_to='files/output/', blank=True)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField('Institution',max_length=100)
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['user']

    def __str__(self):
        return '{}'.format(self.user.username)

def save(self, *args, **kwargs):
    super(Profile, self).save(*args, **kwargs)

    # company = models.ForeignKey(Company, related_name="companies")

    #apps = models.ManyToManyField(App, blank=True, related_name="apps")


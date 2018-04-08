# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

# Create your models here.

def image_upload_location(instance, filename):
    return 'app/%s.png' % (instance.id)

class ImageSlideshow(models.Model):
    image = models.ImageField('Image', upload_to=image_upload_location)
    title = models.CharField('Title', max_length=100)

class MyCompany(models.Model):
    logo = models.ImageField('Logo', blank=True, null=True, upload_to=image_upload_location)
    name = models.CharField('Name', max_length=100)
    # description = models.CharField('Description', max_length=100)
    address = models.TextField('Address', blank=True)
    phone = models.CharField('Phone', blank=True, max_length=9)
    email = models.EmailField('Email')
    citations = models.TextField('Citations')

class App(models.Model):
    taskcode = models.CharField('TaskCode', max_length=100, blank=True, null=True)
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description', blank=True, null=True)
    citation = models.TextField('Citation', blank=True, null=True)
    image = models.ImageField('Image', blank=True, null=True, upload_to=image_upload_location)
    command = models.CharField('Command', max_length=100, blank=False)
    app_compatibility = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Section(models.Model):
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Section')
    subsection = models.ForeignKey('self',blank=True, null=True)
    app = models.ForeignKey(App, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.title)


class Task(models.Model):
    LIST_STATES = (('pending','Pending'),('in_queue','In Queue'),('completed','Completed'),('canceled','Canceled'))

    taskcode = models.CharField('TaskCode', max_length=100)
    name = models.CharField('Name', max_length=100)
    state = models.CharField(
        max_length=15,
        choices=LIST_STATES,
        default='pending',
    )
    app = models.ForeignKey(App, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    creation_date = models.DateTimeField('Creation Date',auto_now_add=True)
    file_input = models.FileField('File Input', upload_to='files/input/',blank=False)
    file_output = models.FileField('File Output', upload_to='files/output/', blank=True)

class ParamsInput(models.Model):
    LIST_INPUT = (
    ('text', 'Text'), ('file', 'File'), ('read', 'Read'))

    name = models.CharField('Name', max_length=100)
    option = models.CharField('Option', max_length=100)
    value = models.CharField('Value', max_length=100)
    state = models.CharField(
        max_length=15,
        choices=LIST_INPUT,
        default='text',
    )
    allowed_format = models.CharField('Allowed Format', max_length=100)
    app = models.ForeignKey(App, related_name="param_app")
    is_required = models.BooleanField('Required')
    is_file_input = models.BooleanField('Is File Input')
    is_file_output = models.BooleanField('Is File Output')
    info = models.TextField('Info')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField('Institution',max_length=100, blank=True, null=True)
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['user']

    def __str__(self):
        return '{}'.format(self.user.username)

def save(self, *args, **kwargs):
    super(Profile, self).save(*args, **kwargs)

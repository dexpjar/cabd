# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from app.models import Profile, App, ParamsInput, Task

# class AppAdmin(admin.ModelAdmin):
#     list_display = ('email','password')
#     list_filter = ('email',)

admin.site.register(Profile)
admin.site.register(App)
admin.site.register(ParamsInput)
admin.site.register(Task)

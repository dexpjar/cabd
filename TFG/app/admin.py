# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from app.models import Profile, App, ParamsInput, Task, Section, ImageSlideshow, MyCompany

# class AppAdmin(admin.ModelAdmin):
#     list_display = ('email','password')
#     list_filter = ('email',)

admin.site.register(Section)
admin.site.register(ParamsInput)
admin.site.register(ImageSlideshow)
admin.site.register(MyCompany)
admin.site.register(App)
admin.site.register(Task)
admin.site.register(Profile)

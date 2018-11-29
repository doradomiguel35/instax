# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import FeedModel,CommentModel

class FeedAdmin(admin.ModelAdmin):
	list_display = ['username','likes']

class CommentAdmin(admin.ModelAdmin):
	list_display = ['comment']

admin.site.register(FeedModel,FeedAdmin)
admin.site.register(CommentModel,CommentAdmin)

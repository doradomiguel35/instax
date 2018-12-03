# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import FeedModel,CommentModel,LikesModel

class FeedAdmin(admin.ModelAdmin):
	list_display = ['username','caption','likes']

class CommentAdmin(admin.ModelAdmin):
	list_display = ['post','username','comment','commented_at']

admin.site.register(FeedModel,FeedAdmin)
admin.site.register(CommentModel,CommentAdmin)
admin.site.register(LikesModel)
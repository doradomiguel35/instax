from django.contrib import admin
from .models import Feeds,Comments,LikesUser

class FeedAdmin(admin.ModelAdmin):
	list_display = ['user','caption','likes']

class CommentAdmin(admin.ModelAdmin):
	list_display = ['post','user','comment','commented_at']

admin.site.register(Feeds,FeedAdmin)
admin.site.register(Comments,CommentAdmin)
admin.site.register(LikesUser)
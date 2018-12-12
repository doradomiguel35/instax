from django.contrib import admin
from .models import Feeds,Comments,LikesUser


class FeedAdmin(admin.ModelAdmin):
	"""
	Feed Admin

	"""
	list_display = ['user','caption','likes']


class CommentAdmin(admin.ModelAdmin):
	"""
	Commen Admin

	"""
	list_display = ['post','user','comment','commented_at']


class LikesAdmin(admin.ModelAdmin):
	"""
	Likes Admin
	"""
	list_display = ['feed','user','liked']


admin.site.register(Feeds,FeedAdmin)
admin.site.register(Comments,CommentAdmin)
admin.site.register(LikesUser,LikesAdmin)
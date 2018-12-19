from django.contrib import admin
from .models import Account,Followers

class AccountsAdmin(admin.ModelAdmin):
	list_display = ['user','followers','prof_pic',]

class FollowersAdmin(admin.ModelAdmin):
	list_display = ['followed_user','follower_username','follow']

admin.site.register(Account,AccountsAdmin)
admin.site.register(Followers,FollowersAdmin)

from django.contrib import admin
from .models import Account,Followers

class AccountsAdmin(admin.ModelAdmin):
	list_display = ['user','followers','prof_pic',]


admin.site.register(Account,AccountsAdmin)
admin.site.register(Followers)

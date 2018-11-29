# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import AccountsModel

class AccountsAdmin(admin.ModelAdmin):
	list_display = ['first_name','last_name','username','email_address','password','phone_num',]

admin.site.register(AccountsModel,AccountsAdmin)
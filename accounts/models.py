from __future__ import unicode_literals
from django.db import models


class AccountsModel(models.Model):
	first_name = models.CharField(max_length=255,default=None)
	last_name = models.CharField(max_length=255,default=None)
	username = models.CharField(max_length=255)
	email_address = models.EmailField()
	password = models.CharField(max_length=50)
	phone_num = models.CharField(max_length=12)
	followers = models.IntegerField(default=0)
	prof_pic = models.ImageField(upload_to='prof_pic',blank=True)

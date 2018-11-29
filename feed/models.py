# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import AccountsModel

class FeedModel(models.Model):
	username = models.ForeignKey(AccountsModel, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='insta_pics',blank = True)
	likes = models.IntegerField(default=0)
	caption = models.TextField(blank=True)


class CommentModel(models.Model):
	post = models.ForeignKey(FeedModel,on_delete=models.CASCADE)
	comment = models.TextField()

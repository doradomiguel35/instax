# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import AccountsModel
from user_profile.models import PicturesUser


class FeedModel(models.Model):
	"""
	Feed
	
	"""
	
	username = models.ForeignKey(AccountsModel, on_delete=models.CASCADE)
	images = models.ForeignKey(PicturesUser,on_delete=models.CASCADE,blank = True,null=True)
	likes = models.IntegerField(default=0)
	caption = models.TextField(blank=True)


class CommentModel(models.Model):
	"""
	Comment
	
	"""

	post = models.ForeignKey(FeedModel,on_delete=models.CASCADE)
	username = models.ForeignKey(AccountsModel, on_delete=models.CASCADE)
	comment = models.TextField()
	commented_at = models.DateTimeField(auto_now_add=True)


class LikesModel(models.Model):
	"""
	Likes
	
	"""

	feed = models.ForeignKey(FeedModel, on_delete=models.CASCADE)
	username = models.ForeignKey(AccountsModel,on_delete=models.CASCADE)
	




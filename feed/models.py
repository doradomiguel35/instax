from django.db import models
from django.contrib.auth.models import User
from user_profile.models import PicturesUser
from accounts.models import Account


class Feeds(models.Model):
	"""
	Feed
	
	"""
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	images = models.ForeignKey(PicturesUser,on_delete=models.CASCADE,blank = True,null=True)
	likes = models.IntegerField(default=0)
	liker = models.ManyToManyField(Account,blank=True)
	liked = models.ManyToManyField('LikesUser',blank=True)
	caption = models.TextField(blank=True)
	archived = models.BooleanField(default=False)


class Comments(models.Model):
	"""
	Comment
	
	"""
	
	post = models.ForeignKey(Feeds,on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	commented_at = models.DateTimeField(auto_now_add=True)
	archived_comment = models.BooleanField(default=False)


class LikesUser(models.Model):
	"""
	Likes
	
	"""
	
	feed = models.ForeignKey(Feeds, on_delete=models.CASCADE,null=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	liked = models.BooleanField(default=False)
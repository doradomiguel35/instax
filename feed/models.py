from django.db import models
from django.contrib.auth.models import User
from user_profile.models import PicturesUser
# Create your models here.
class Feeds(models.Model):
	"""
	Feed
	
	"""
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	images = models.ForeignKey(PicturesUser,on_delete=models.CASCADE,blank = True,null=True)
	likes = models.IntegerField(default=0)
	caption = models.TextField(blank=True)


class Comments(models.Model):
	"""
	Comment
	
	"""
	
	post = models.ForeignKey(Feeds,on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	commented_at = models.DateTimeField(auto_now_add=True)


class LikesUser(models.Model):
	"""
	Likes
	
	"""
	
	feed = models.ForeignKey(Feeds, on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
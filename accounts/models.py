from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
	"""
	Accounts model
	
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	followers = models.IntegerField(default=0)
	prof_pic = models.ImageField(upload_to='prof_pic',blank=True,null=True)


class Followers(models.Model):
	"""
	Followers
	
	"""

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	follow = models.BooleanField(default=False)




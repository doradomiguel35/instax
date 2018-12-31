from django.db import models


from django.contrib.auth.models import User

# Create your models here.
class PicturesUser(models.Model):
	"""
	Pictures of the user 
	"""

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	image = models.ImageField(upload_to='insta_pics')



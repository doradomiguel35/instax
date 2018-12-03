from django.db import models
from accounts.models import AccountsModel
from feed.models import FeedModel


class PicturesUser(models.Model):
	username = models.ForeignKey(AccountsModel,on_delete=models.CASCADE)
	feed = models.ForeignKey(FeedModel,on_delete=models.CASCADE)
	


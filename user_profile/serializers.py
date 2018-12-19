from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Account


class UserSerialize(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
			'username',
			'email',
		)

class ProfPicSerialize(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = (
			'prof_pic',
			'followers',
			'following',
		)
from rest_framework import serializers
from .models import Followers,Account


class FollowerSerializer(serializers.ModelSerializer):
	"""
	Followers Serializer

	"""
	class Meta:
		model = Followers
		fields = (
			'id',
			'followed_user_id',
			'follower_username_id',
			'follow'
		)
		
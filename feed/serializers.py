from rest_framework import serializers
from feed.models import Comments,Feeds,LikesUser


class CommentSerialize(serializers.ModelSerializer):
	"""
	Comment Serializer

	"""
	class Meta:
		model = Comments
		fields = (
			'id',
			'post_id',
			'user_id',
			'comment',
			'commented_at')


class FeedSerialize(serializers.ModelSerializer):
	"""
	Feed Serializer

	"""
	class Meta:
		model = Feeds
		fields = (
			'id',
			'user_id',
			'likes',
			'caption')


class LikesSerialize(serializers.ModelSerializer):
	"""
	Likes Serializer

	"""		
	class Meta:
		model = LikesUser
		fields = (
			'id',
			'feed_id',
			'user_id',
			'liked')


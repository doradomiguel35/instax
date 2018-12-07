from rest_framework import serializers
from feed.models import CommentModel


class CommentSerialize(serializers.ModelSerializer):
	"""
	Comment Serializer

	"""
	class Meta:
		model = CommentModel
		fields = (
			'id',
			'post_id',
			'username_id',
			'comment',
			'commented_at')
		

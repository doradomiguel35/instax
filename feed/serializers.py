from rest_framework import serializers
from feed.models import Comments


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
		

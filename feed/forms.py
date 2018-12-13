from django import forms
from .models import Comments,LikesUser,Feeds
from user_profile.models import PicturesUser


class CommentForm(forms.ModelForm):
	"""
	Comment Form, comment on posts

	"""

	comment = forms.CharField(max_length=255, label='',widget=forms.Textarea(attrs={
		'id':'create-comment-field',
		'placeholder':('Place Comments Here'),
		'rows':5,
		'cols': 82,
		'style': "margin-left: 0px;border: 1px solid grey;border-radius: 10px;",
		}))


	class Meta:
		model = Comments
		fields = ('comment',)

	def clean(self):
		return self.cleaned_data


class LikeForm(forms.ModelForm):
	"""
	Like Form, like on posts
	"""
	liked = forms.BooleanField(label='',widget=forms.CheckboxInput(attrs={
		'id':'like-button',
		'type':'checkbox',
		}))

	class Meta:
		model = LikesUser
		fields = ('liked',)


class FeedForm(forms.ModelForm):
	"""
	Post Form, create posts

	"""
	caption = forms.CharField(max_length=255, label='',widget=forms.Textarea(attrs={
		'id':'create-caption-field',
		'placeholder':('What is on your mind?'),
		'rows':5,
		'cols': 82,
		'style': "margin-left: 0px;border: 1px solid grey;border-radius: 10px;",
		}))

	class Meta:
		model = Feeds
		fields = ('caption',)



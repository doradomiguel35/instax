from django import forms
from .models import Comments,LikesUser


class CommentForm(forms.ModelForm):
	"""
	Comment Form

	"""

	comment = forms.CharField(widget=forms.Textarea(attrs={
		'id':'create-comment-field',
		'placeholder':('Place Comments Here'),
		'rows':5,
		'cols': 82,
		'style': "margin-left: 0px;border: 1px solid grey;border-radius: 10px;",
		}),max_length=255, label='')


	class Meta:
		model = Comments
		fields = ('comment',)

	def clean(self):
		return self.cleaned_data


class LikeForm(forms.ModelForm):

	liked = forms.BooleanField(widget=forms.CheckboxInput(attrs={
		'id':'like-button',
		'type':'checkbox',
		}),label='')

	class Meta:
		model = LikesUser
		fields = ('liked',)

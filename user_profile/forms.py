from django import forms
from user_profile.models import PicturesUser


class PicturesForm(forms.ModelForm):
	"""
	Picture Form, add picture to gallery or use picture as post

	"""
	image = forms.ImageField()

	class Meta:
		model = PicturesUser
		fields = ('image',)

from django import forms
from user_profile.models import PicturesUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from accounts.models import Account


class PicturesForm(forms.ModelForm):
	"""
	Picture Form, add picture to gallery or use picture as post

	"""
	image = forms.ImageField()

	class Meta:
		model = PicturesUser
		fields = ('image',)


class EditProfileForm(UserChangeForm):
	"""
	Edit Profile Form

	Update profile information
	"""
	
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your First Name')}),max_length=255,label='First Name')
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Last Name')}),max_length=255)
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Username')}),max_length=255)
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':('Enter your Email Address')}),required=True)
	
	class Meta:
		model = User
		fields = ('first_name','last_name','username','email')



class ProfPicForm(forms.ModelForm):
	"""
	Prof Pic Form
	Set/change profile picture
	
	"""
	class Meta:
		model = Account
		fields = ('prof_pic',)


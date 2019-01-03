from django import forms
from django.core.validators import RegexValidator
from django.core import validators
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate


class RegisterValidation(forms.ModelForm):
	"""
	Register Validation
	"""

	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your First Name')}),max_length=255)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Last Name')}),max_length=255)
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Username')}),max_length=255)
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':('Enter your Email Address')}),required=True)
	password = forms.CharField(widget = forms.TextInput(attrs={'placeholder':('Enter your Password'),'type':'password'}),max_length = 50,min_length=2)
	confirm = forms.CharField(widget = forms.TextInput(attrs={'placeholder':('Confirm Password'),'type':'password'}),max_length = 50,min_length=2)
	# account_model = Account.objects.all()
	

	class Meta:
		model = User
		fields = ('first_name','last_name','username','email','password')

	def clean_email(self):
		email = User.objects.filter(email=self.cleaned_data['email'])
		if email.exists():
			raise forms.ValidationError('Email already existed!')
		return self.cleaned_data['email']

	def clean_username(self):
		username = User.objects.filter(username=self.cleaned_data['username'])
		if username.exists():
			raise forms.ValidationError('Username already existed!')
		return self.cleaned_data['username']

	def clean(self):
		password = self.cleaned_data.get('password')
		confirm = self.cleaned_data.get('confirm')

		if password != confirm:
			raise forms.ValidationError('Passwords did not match!')
		return self.cleaned_data

class LoginValidation(forms.Form):
	"""
	Login Validation
	
	"""

	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Username')}),max_length = 255)
	password = forms.CharField(widget = forms.TextInput(attrs={'placeholder':('Enter your Password'),'type':'password'}),max_length = 50,min_length=2)
	# account_model = Account.objects.all()

	class Meta:
		model = User
		fields = ('username','password',)


	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		user = authenticate(username=username,password=password)

		if user is not None:
			return self.cleaned_data
		raise forms.ValidationError('Invalid Username or Password')


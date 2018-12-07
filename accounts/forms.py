from django import forms
from django.core.validators import RegexValidator
from django.core import validators
from .models import AccountsModel
from django.shortcuts import render


class RegisterValidation(forms.ModelForm):
	"""
	Register Validation
	"""

	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your First Name')}),max_length=255)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Last Name')}),max_length=255)
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Username')}),max_length=255)
	email_address = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':('Enter your Email Address')}),required=True)
	phone_num = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter you Phone No.')}),max_length= 17)
	password = forms.CharField(widget = forms.TextInput(attrs={'placeholder':('Enter your Password'),'type':'password'}),max_length = 50,min_length=2)
	confirm = forms.CharField(widget = forms.TextInput(attrs={'placeholder':('Confirm Password'),'type':'password'}),max_length = 50,min_length=2)
	account_model = AccountsModel.objects.all()
	

	class Meta:
		model = AccountsModel
		fields = ('first_name','last_name','username','email_address','phone_num','password',)

	def clean_email_address(self):
		email = AccountsModel.objects.filter(email_address=self.cleaned_data['email_address'])
		if email.exists():
			raise forms.ValidationError('Email already existed!')
		return self.cleaned_data

	def clean_username(self):
		username = AccountsModel.objects.filter(username=self.cleaned_data['username'])
		if username.exists():
			raise forms.ValidationError('Username already existed!')
		return self.cleaned_data	

	def clean(self):
		password = self.cleaned_data['password']
		confirm = self.cleaned_data['confirm']

		if password != confirm:
			raise forms.ValidationError('Passwords did not match!')
		
		return self.cleaned_data


class LoginValidation(forms.Form):
	"""
	Login Validation
	
	"""

	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Username')}),max_length = 255)
	password = forms.CharField(widget = forms.TextInput(attrs={'placeholder':('Enter your Password'),'type':'password'}),max_length = 50,min_length=2)
	account_model = AccountsModel.objects.all()

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		for account in self.account_model:
			if username == account.username and password == account.password:
				return self.cleaned_data
		raise forms.ValidationError('Invalid Username or Password')


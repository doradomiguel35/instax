from django import forms
from django.core.validators import RegexValidator
from django.core import validators
from .models import AccountsModel
from django.shortcuts import render


class RegisterValidation(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your First Name'),'class':'form-control',}),max_length = 255)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Last Name'),'class':'form-control'}),max_length = 255)
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Username'),'class':'form-control'}),max_length = 255)
	email_address = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':('Enter your Email'),'class':'form-control'},),required=True)
	phone_num = forms.CharField(max_length= 17,widget=forms.TextInput(attrs={'placeholder':('Enter your Phone No.'),'class':'form-control','pattern':"[0-9]{9,11}"}))
	password = forms.CharField(max_length = 50,min_length=2,widget = forms.TextInput(attrs={'placeholder':('Enter your Password'),'class':'form-control','type':'password'}))
	confirm = forms.CharField(max_length= 50,min_length=2, widget= forms.TextInput(attrs={'placeholder':('Confirm Password'),'class':'form-control','type':'password'}))
	account_model = AccountsModel.objects.all()
	

	class Meta:
		model = AccountsModel
		fields = ('first_name','last_name','username','email_address','phone_num','password',)

	def clean_email(self):
		email = self.cleaned_data['email']
		
		for account in self.account_model:
			if email == account.email_address:
				raise forms.ValidationError('Email already existed!')
		return email

	def clean_username(self):
		username = self.cleaned_data['username']

		for account in self.account_model:
			if username == account.username:
				raise forms.ValidationError('Username already existed!')
		return username

	def clean(self):
		password = self.cleaned_data['password']
		confirm = self.cleaned_data['confirm']

		if password != confirm:
			raise forms.ValidationError('Passwords did not match!')
		
		return self.cleaned_data



	
class LoginValidation(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Enter your Username'),'class':'form-control'}),max_length = 255)
	password = forms.CharField(max_length = 50,min_length=2,widget = forms.TextInput(attrs={'placeholder':('Enter your Password'),'class':'form-control','type':'password'}))
	account_model = AccountsModel.objects.all()

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		for account in self.account_model:
			if username == account.username and password == account.password:
				return self.cleaned_data
		raise forms.ValidationError('Invalid Username or Password')


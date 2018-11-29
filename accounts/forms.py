from django import forms


class AccountsForm(forms.Form):
	first_name = forms.CharField(max_length = 255)
	last_name = forms.CharField(max_length = 255)
	username = forms.CharField(max_length = 255)
	email_address = forms.EmailField()
	password = forms.CharField(max_length = 50,widget = forms.PasswordInput())

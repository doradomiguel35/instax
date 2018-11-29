from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from .models import AccountsModel
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import AccountsForm


class RegisterView(View):
	template_name = 'accounts/register.html'
	context = AccountsModel.objects.all()
	forms = AccountsForm()
	def get(self, *args, **kwargs):
	    return render(self.request,self.template_name, {'context_data': self.context,'forms':forms})

	def post(self, *args, **kwargs):
		account_form = AccountsModel()
		if self.request.method == 'POST':
			if self.request.POST.get('fname') and self.request.POST.get('lname') and self.request.POST.get('email') and self.request.POST.get('username') and self.request.POST.get('password') and self.request.POST.get('phone_num'):
				account_form.first_name = self.request.POST.get('fname')
				account_form.last_name = self.request.POST.get('lname')
				account_form.email_address = self.request.POST.get('email')
				account_form.username = self.request.POST.get('username')
				account_form.phone_num = self.request.POST.get('phone_num')
				account_form.password = self.request.POST.get('password')

				for account in self.context:
					if self.request.POST.get('email') == account.email_address or self.request.POST.get('username') == account.username:
						return HttpResponse('Email address/Username already exists')


				if account_form.password != self.request.POST.get('confirm'):
					return HttpResponse('Password did not match')

				else:
					account_form.save()
					return render(self.request,'feed/users_page.html')
		else:
			return HttpResponse('Account Denied')


class LoginView(View):
	template_name = 'accounts/login.html'
	context = AccountsModel.objects.all()
		
	def get(self,*args,**kwargs):
		return render(self.request, self.template_name,{'context_data': self.context})

	def post(self, *args, **kwargs):
		if self.request.method == 'POST':
			if self.request.POST.get('username') and self.request.POST.get('password'):
				for account in self.context:
					if self.request.POST.get('username') == account.username and self.request.POST.get('password') == account.password:
						return render(self.request,'feed/')
				return HttpResponse('Incorrect password or email!')
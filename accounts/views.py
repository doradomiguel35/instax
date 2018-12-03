from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from .models import AccountsModel
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import RegisterValidation,LoginValidation
from django import forms
from feed.models import FeedModel,CommentModel


class RegisterView(View):
	template_name = 'accounts/register.html'
	context = AccountsModel.objects.all()
	feed_data = FeedModel.objects.all()
	comment_data = CommentModel.objects.all()
	get_forms = RegisterValidation()

	def get(self, *args, **kwargs):
		return render(self.request,self.template_name, {'context_data': self.context,'forms':self.get_forms})

	def post(self,request, *args, **kwargs):
		form = RegisterValidation(request.POST)
		if form.is_valid():
			print(form.save())
			return render(request,'feed/users_page.html',{'context_data': self.context,'feed_data':self.feed_data,'comment_data':self.comment_data,'forms':form})
		return render(request,'accounts/register.html',{'context_data': self.context,'forms':form}) 


class LoginView(View):
	template_name = 'accounts/login.html'
	context = AccountsModel.objects.all()
	feed_data = FeedModel.objects.all()
	comment_data = CommentModel.objects.all()
	get_forms = LoginValidation()
	
	def get(self,*args,**kwargs):
		return render(self.request, self.template_name,{'context_data': self.context,'forms':self.get_forms})

	def post(self, *args, **kwargs):
		forms = LoginValidation(self.request.POST)
		if forms.is_valid():
			filter_data = AccountsModel.objects.filter(username=self.request.POST.get('username'))	
			# import pdb; pdb.set_trace()

			return render(self.request,'feed/users_page.html',{'context_data': self.context,'feed_data':self.feed_data,'comment_data':self.comment_data,'forms':forms})
		return render(self.request, 'accounts/error/error_login.html',{'context': self.context,'error': "Invalid username or password!",'forms':forms })

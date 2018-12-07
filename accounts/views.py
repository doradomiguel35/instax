from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from .models import AccountsModel
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import RegisterValidation,LoginValidation
from feed.forms import CommentForm
from django import forms
from feed.models import FeedModel,CommentModel


class RegisterView(TemplateView):
	"""
	Register View
	
	"""

	template_name = 'accounts/register.html'
	context = AccountsModel.objects.all()
	feed_data = FeedModel.objects.all()
	comment_data = CommentModel.objects.all()
	get_forms = RegisterValidation()

	def get(self, *args, **kwargs):
		return render(self.request,self.template_name, {'context_data': self.context,'forms':self.get_forms})

	def post(self,request, *args, **kwargs):
		form = RegisterValidation(request.POST)
		comment_form = CommentForm()
		if form.is_valid():
			form.save()
			filter_data = AccountsModel.objects.get(username=self.request.POST.get('username'))		
			return render(request,'base.html',{'context_data': self.context,'feed_data':self.feed_data,'comment_data':self.comment_data,'user_data':filter_data,'comment_form':comment_form})
		return render(request,'accounts/register.html',{'context_data': self.context,'forms':form}) 


class LoginView(TemplateView):
	"""
	Login View

	"""

	template_name = 'accounts/login.html'
	context = AccountsModel.objects.all()
	feed_data = FeedModel.objects.all()
	comment_data = CommentModel.objects.all()
	get_forms = LoginValidation()
	
	def get(self,*args,**kwargs):
		return render(self.request, self.template_name,{'context_data': self.context,'forms':self.get_forms})

	def post(self,request, *args, **kwargs):
		forms = LoginValidation(self.request.POST)
		comment_form = CommentForm()
		if forms.is_valid():
			filter_data = AccountsModel.objects.get(username=self.request.POST.get('username'))	
			return render(request,'base.html',{'context_data': self.context,'feed_data':self.feed_data,'comment_data':self.comment_data,'forms':forms,'user_data': filter_data,'comment_form':comment_form})
		return render(request, 'accounts/error/error_login.html',{'context': self.context,'error': "Invalid username or password!",'forms':forms })

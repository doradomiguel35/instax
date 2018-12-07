# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from .models import FeedModel,CommentModel
from accounts.models import AccountsModel,FollowersModel
from user_profile.models import PicturesUser
from .forms import CommentForm
from django.http import JsonResponse
from .serializers import CommentSerialize

from django.shortcuts import render

class FeedsView(TemplateView):
	"""
	Feeds View

	"""
	template_name = 'feed/users_page.html'
	feed_data = FeedModel.objects.all()
	comment_data = CommentModel.objects.all()
	comment_form = CommentForm()
	
		
	def get(self, *args, **kwargs):
		user_data = AccountsModel.objects.get(username=kwargs.get('username'))
		
		return render(self.request, self.template_name,{'feed_data': self.feed_data,'comment_data':self.comment_data,'user_data':user_data,'comment_form':self.comment_form})

	def post(self,request, *args, **kwargs):
		form = CommentForm(self.request.POST)	
		feed = FeedModel.objects.get(id=kwargs.get('feed_id'))
		account = AccountsModel.objects.get(username=kwargs.get('username'))
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post_id = feed.id
			comment.username_id = account.id 
			comment.save()
			serializer = CommentSerialize(CommentModel.objects.get(id=comment.id))
			return JsonResponse(serializer.data, safe=False)


class FeedUser(TemplateView):
	template_name = 'feed/feed_user.html'
	followers = FollowersModel.objects.all()

	def get(self,request, *args,**kwargs):
		username = kwargs.get('username')
		profile = kwargs.get('profile')
		profile_user = AccountsModel.objects.get(username=profile)
		account = AccountsModel.objects.get(username=username)
		pictures = PicturesUser.objects.filter(username_id=profile_user.id)
		try: 	
			account.prof_pic.url
			return render(request,self.template_name,{'profile':profile_user,'user_data': account,'followers':self.followers,'no_prof_pic': False,'pictures':pictures})
		except:
			return render(request,self.template_name,{'profile':profile_user,'user_data': account,'followers':self.followers,'no_prof_pic': True,'pictures':pictures})


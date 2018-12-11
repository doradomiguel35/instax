from __future__ import unicode_literals
from django.views.generic import TemplateView
from .models import Feeds,Comments
from accounts.models import Account,Followers
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
	feed_data = Feeds.objects.all()
	comment_data = Comments.objects.all()
	comment_form = CommentForm()
	
		
	def get(self, *args, **kwargs):
		return render(self.request, self.template_name,{'feed_data': self.feed_data,'comment_data':self.comment_data,'user_data':self.request.user,'comment_form':self.comment_form})

	def post(self,request, *args, **kwargs):
		form = CommentForm(self.request.POST)	
		feed = Feeds.objects.get(id=kwargs.get('feed_id'))
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post_id = feed.id
			comment.user_id = self.request.user.id
			comment.save()
			serializer = CommentSerialize(Comments.objects.get(id=comment.id))
			json = serializer.data
			json['username'] = self.request.user.username
			return JsonResponse(json, safe=False)
from __future__ import unicode_literals
from django.views.generic import TemplateView,View
from .models import Feeds,Comments,LikesUser
from accounts.models import Account,Followers
from user_profile.models import PicturesUser
from .forms import CommentForm,LikeForm
from django.http import JsonResponse
from .serializers import CommentSerialize,FeedSerialize,LikesSerialize
from django.shortcuts import render


class FeedsView(TemplateView):
	"""
	Feeds View

	"""
	template_name = 'feed/users_page.html'
	feed_data = Feeds.objects.all()
	comment_data = Comments.objects.all()
	comment_form = CommentForm()
	like_field = LikeForm()
	
	def get(self, *args, **kwargs):
		self.comment_data._result_cache = None
		self.feed_data._result_cache = None

		return render(self.request, self.template_name,{
			'feed_data': self.feed_data,'comment_data':self.comment_data,'user_data':self.request.user,'comment_form':self.comment_form,'like_field':self.like_field})

	def post(self,request, *args, **kwargs):
		form = CommentForm(self.request.POST)	
		feed = Feeds.objects.get(id=kwargs.get('feed_id'))
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post_id = feed.id
			comment.user_id = self.request.user.id
			comment.save()
			comment.refresh_from_db()
			serializer = CommentSerialize(Comments.objects.get(id=comment.id))
			json = serializer.data
			json['username'] = self.request.user.username
			
			return JsonResponse(json, safe=False)


class LikeView(TemplateView):
	"""
	Likes View

	"""
	
	def post(self,request,*args,**kwargs):
		feed_data = Feeds.objects.get(id=kwargs.get('feed_id'))
		like_user = LikesUser.objects.get(feed_id=kwargs.get('feed_id'),user_id=self.request.user.id)
		# import pdb; pdb.set_trace()
		try:
			print('try')
			if like_user.liked == True:
				print('if')
				feed_data.likes-=1
				like_user.liked = False
				feed_data.save()
				like_user.save()
				feed_serializer = FeedSerialize(feed_data)
				json = feed_serializer.data
				return JsonResponse(json, safe=False)
				
			else:
				print('else')
				feed_data.likes+=1
				like_user.liked = True
				feed_data.save()
				like_user.save()
				feed_serializer = FeedSerialize(feed_data)
				json = feed_serializer.data
				return JsonResponse(json, safe=False)
				
		except:
			print('exception')
			like_user = LikesUser(feed_id=kwargs.get('feed_id'),user_id=self.request.user.id,liked=True)
			like_user.save()
			feed_data.likes+=1
			feed_data.save()
			feed_serializer = FeedSerialize(feed_data)
			json = feed_serializer.data
			return JsonResponse(json, safe=False)

			

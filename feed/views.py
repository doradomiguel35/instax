from __future__ import unicode_literals
from django.views.generic import TemplateView,View
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.models import User
from .models import Feeds,Comments,LikesUser
from accounts.models import Account,Followers
from user_profile.models import PicturesUser
from feed.forms import CommentForm,FeedForm
from user_profile.forms import PicturesForm
from .forms import CommentForm,LikeForm
from .serializers import CommentSerialize,FeedSerialize,LikesSerialize


class FeedsView(TemplateView):
	"""
	Feeds View
	GET - render template, send context data
	POST - return json response to display recently added comments

	"""
	template_name = 'feed/users_page.html'
	feed_data = Feeds.objects.all().order_by('-id')
	comment_data = Comments.objects.all()
	comment_form = CommentForm()
	like_field = LikeForm()
	feed_form = FeedForm()
	picture_form = PicturesForm()
	
	
	def get(self, *args, **kwargs):
		self.comment_data._result_cache = None
		self.feed_data._result_cache = None

		return render(
			self.request, 
			self.template_name,
			{'feed_data': self.feed_data,
			'comment_data':self.comment_data,
			'user_data':self.request.user,
			'comment_form':self.comment_form,
			'feed_form':self.feed_form,
			'picture_form':self.picture_form,}
		)

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
			serialized = serializer.data
			serialized['username'] = self.request.user.username
			
			return JsonResponse(serialized, safe=False)


class LikeView(View):
	"""
	Likes View 
	GET - retrieve username and prof pic, return json to display accounts that liked the post
	POST - each user can like a post once, if a post is already liked, then the user clicked the like button, it will be unliked

	"""
	def get(self,request,*args,**kwargs):
		likers = LikesUser.objects.filter(feed_id=kwargs.get('feed_id'),liked=True).values('user__username','user__account__prof_pic')
		serializer = {'data': list(likers)}
		return JsonResponse(serializer, safe=False)
		

	def post(self,request,*args,**kwargs):
		feed_data = Feeds.objects.get(id=kwargs.get('feed_id'))
		
		try:
			like_user = LikesUser.objects.get(feed_id=kwargs.get('feed_id'),user_id=self.request.user.id)
			print('try')
			if like_user.liked == True:
				print('if')
				feed_data.likes-=1
				like_user.liked = False
				feed_data.save()
				like_user.save()
				feed_serializer = FeedSerialize(feed_data)
				serialized = feed_serializer.data
				return JsonResponse(serialized, safe=False)
				
			else:
				print('else')
				feed_data.likes+=1
				like_user.liked = True
				feed_data.save()
				like_user.save()
				feed_serializer = FeedSerialize(feed_data)
				serialized = feed_serializer.data
				return JsonResponse(serialized, safe=False)
				
		except:
			print('exception')
			like_user = LikesUser(feed_id=kwargs.get('feed_id'),user_id=self.request.user.id,liked=True)
			feed_data.likes+=1
			like_user.save()
			feed_data.save()
			feed_serializer = FeedSerialize(feed_data)
			serialized = feed_serializer.data
			return JsonResponse(serialized, safe=False)


class CreatePost(View):
	"""
	Create Posts
	POST - return json response to display newly created posts

	"""
	def post(self, request,*args,**kwargs):
		caption = FeedForm(request.POST)
		image = PicturesForm(data=request.POST,files=request.FILES)
		
		if caption.is_valid() and image.is_valid():
			caption = caption.save(commit=False)
			image = image.save(commit=False)
			image.user_id = request.user.id
			image.save()
			caption.user_id = request.user.id
			caption.images_id = image.id
			caption.save()
			serialize = FeedSerialize(caption)
			new_post = serialize.data
			new_post['username'] = caption.user.username
			new_post['image'] = caption.images.image.url
			try:
				new_post['prof_pic'] = caption.user.account.prof_pic.url
				return JsonResponse(new_post, safe=False)
			except:
				return JsonResponse(new_post, safe=False)
from __future__ import unicode_literals
from django.views.generic import TemplateView,View
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.models import User
from .models import Feeds,Comments,LikesUser
from accounts.models import Account,Followers
from user_profile.models import PicturesUser
from feed.forms import CommentForm,FeedForm,SearchForm
from user_profile.forms import PicturesForm
from .serializers import CommentSerialize,FeedSerialize,LikesSerialize


class FeedsView(TemplateView):
	"""
	Feeds View
	GET - render template, send context data
	POST - return json response to display recently added comments

	"""
	template_name = 'feed/users_page.html'
	comment_data = Comments.objects.all()
	comment_form = CommentForm()	
	feed_form = FeedForm()
	picture_form = PicturesForm()
	search_form = SearchForm()
	
	
	def get(self,request, *args, **kwargs):
		followers = Followers.objects.filter(follow=True,follower_username=request.user.username).values('followed_user_id')
		import pdb;pdb.set_trace()
		feed_data = Feeds.objects.filter(user_id__in=followers)
		feed_data._result_cache = None
		self.comment_data._result_cache = None
		return render(
			request, 
			self.template_name,
			{'feed_data': feed_data,
			'comment_data':self.comment_data,
			'user_data':self.request.user,
			'comment_form':self.comment_form,
			'feed_form':self.feed_form,
			'picture_form':self.picture_form,
			'search_form':self.search_form,
			'current_user':self.request.user,}
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
		likers = LikesUser.objects.filter(
				feed_id=kwargs.get('feed_id'),
				liked=True
			).values(
				'user__username',
				'user__account__prof_pic')
		
		serializer = {'data': list(likers)}
		return JsonResponse(serializer, safe=False)
		

	def post(self,request,*args,**kwargs):
		feed_data = Feeds.objects.get(id=kwargs.get('feed_id'))
		
		try:
			like_user = LikesUser.objects.get(feed_id=kwargs.get('feed_id'),user_id=self.request.user.id)
			if like_user.liked == True:
				feed_data.likes-=1
				like_user.liked = False
				feed_data.save()
				like_user.save()
				feed_serializer = FeedSerialize(feed_data)
				serialized = feed_serializer.data
				return JsonResponse(serialized, safe=False)
				
			else:
				feed_data.likes+=1
				like_user.liked = True
				feed_data.save()
				like_user.save()
				feed_serializer = FeedSerialize(feed_data)
				serialized = feed_serializer.data
				return JsonResponse(serialized, safe=False)
				
		except:
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


class Search(View):
	"""
	Search
	GET - search for users, return json response to acquire searched user

	"""
	def get(self,request,*args,**kwargs):
		search_form = SearchForm(self.request.GET)

		if search_form.is_valid():
			search_username = Account.objects.filter(user__username=search_form.cleaned_data['search']).values('user__username','prof_pic')
			serialize = {'data': list(search_username)}
			return JsonResponse(serialize,safe=False)
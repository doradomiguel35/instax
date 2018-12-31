from __future__ import unicode_literals
from django.views.generic import TemplateView,View
from django.views.generic.detail import DetailView
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
	comment_form = CommentForm()	
	feed_form = FeedForm()
	picture_form = PicturesForm()
	search_form = SearchForm()
	
	
	def get(self,request, *args, **kwargs):
		followers = Followers.objects.filter(follow=True,follower_username=request.user.username).values('followed_user_id')
		
		feed_data = Feeds.objects.filter(user_id__in=followers,archived=False) | Feeds.objects.filter(user_id=request.user.id,archived=False)
	
		comment_data = Comments.objects.filter(post_id__in=feed_data.values('id'))
			
		feed_data._result_cache = None
		
		comment_data._result_cache = None
		
		package = {
			'feed_data': feed_data.order_by('-id'),
			'comment_data':comment_data,
			'user_data':request.user,
			'comment_form':self.comment_form,
			'feed_form':self.feed_form,
			'picture_form':self.picture_form,
			'search_form':self.search_form,
			'current_user':self.request.user,
		}
		
		return render(
			request, 
			self.template_name,
			package
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
			serialized['username'] = comment.user.username
			serialized['current_user'] = request.user.username
			
			return JsonResponse(serialized, safe=False)


class LikeView(View):
	"""
	Likes View 
	GET - retrieve username and prof pic, return json to display accounts that liked the post
	POST - each user can like a post once, if a post is already liked, then the user clicked the like button, it will be unliked

	"""

	def get(self,request,*args,**kwargs):

		feed_likers = Feeds.objects.get(
			id=kwargs.get('feed_id')).liker.all().values(
					'user__username',
					'prof_pic'
				)
		
		serializer = {
			'data': list(feed_likers)
		}
		
		return JsonResponse(serializer, safe=False)
		

	def post(self,request,*args,**kwargs):

		feed_data = Feeds.objects.get(id=kwargs.get('feed_id'))
		# like_user = LikesUser.objects.get(feed_id=kwargs.get('feed_id')).liked.filter(user_id=request.user.id)
		
		try:
			like_user = Feeds.objects.get(id=kwargs.get('feed_id')).liked.get(user_id=request.user.id)
			account_user = Account.objects.get(user_id=self.request.user.id)
			
			if like_user.liked == True:
				feed_data.likes-=1
				feed_data.liker.remove(account_user)
				like_user.liked = False
				like_user.save()
				feed_data.liked.add(like_user)
				feed_data.save()
				feed_serializer = FeedSerialize(feed_data)
				serialized = feed_serializer.data
				return JsonResponse(serialized, safe=False)
				
			else:
				feed_data.likes+=1
				feed_data.liker.add(account_user)
				like_user.liked = True
				like_user.save()
				feed_data.liked.add(like_user)
				feed_data.save()
				feed_serializer = FeedSerialize(feed_data)
				serialized = feed_serializer.data
				return JsonResponse(serialized, safe=False)
				
		except:
			account_user = Account.objects.get(user_id=self.request.user.id)
			like_user = LikesUser(feed_id=kwargs.get('feed_id'),user_id=self.request.user.id,liked=True)
			feed_data.likes+=1
			feed_data.liker.add(account_user)	
			like_user.save()
			feed_data.liked.add(like_user)
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


class ArchivePost(View):
	"""
	POST - archive post, not completely deleting the post, instead view archived posts in edit profile menu
	"""

	def post(self,request,*args,**kwargs):
		feed = Feeds.objects.get(id=kwargs.get('feed_id'))
		feed.archived = True
		feed.save()
		feed_serialize = FeedSerialize(feed)
		serialized = feed_serialize.data
		return JsonResponse(serialized,safe=False)


class EditPost(View):
	"""
	GET - get edit forms, to display in template view
	POST - save recently edited object, returns JSON response to display in template view
	"""
	def get(self,request,*args,**kwargs):
		feed = Feeds.objects.get(id=kwargs.get('feed_id'))
		image = PicturesUser.objects.get(id=kwargs.get('image_id'))
		feed_serialize = FeedSerialize(feed)
		serialized = feed_serialize.data
		serialized['image'] = image.image.url
		serialized['username'] = feed.user.username

		return JsonResponse(serialized,safe=False)


	def post(self, request, *args, **kwargs):
		feed = Feeds.objects.get(id=kwargs.get('feed_id'))
		image = PicturesUser.objects.get(id=kwargs.get('image_id'))
		feed_form = FeedForm(request.POST,instance=feed)
		image_form = PicturesForm(data=request.POST,files=request.FILES,instance=image)
		
		if feed_form.is_valid() and image_form.is_valid():
			feed_form.save()
			image_form.save()

			serialize_feed = FeedSerialize(Feeds.objects.get(id=kwargs.get('feed_id'))).data
			image_new = PicturesUser.objects.get(id=kwargs.get('image_id'))
			serialize_feed['image'] = image_new.image.url
			serialize_feed['username'] = feed.user.username
			return JsonResponse(serialize_feed,safe=False)


class EditComment(View):
	"""
	Edit Comments
	"""
	def get(self,request,*args,**kwargs):
		comment = Comments.objects.get(id=kwargs.get('comment_id'))
		comment_serialize = CommentSerialize(comment).data

		return JsonResponse(comment_serialize,safe=False)


	def post(self,request,*args,**kwargs):
		comment = Comments.objects.get(id=kwargs.get('comment_id'))
		comment_form = CommentForm(request.POST,instance=comment)

		if comment_form.is_valid():
			comment_form.save()
			
			comment_serialize = CommentSerialize(Comments.objects.get(id=kwargs.get('comment_id'))).data

			comment_serialize['username'] = comment.user.username
			comment_serialize['current_user'] = request.user.username
			return JsonResponse(comment_serialize,safe=False)


class DeleteComment(View):
	"""
	Delete COmments

	"""

	def post(self,request,*args,**kwargs):
		comment = Comments.objects.get(id=kwargs.get('comment_id'))
		comment_serialize = CommentSerialize(comment).data
		comment_serialize['username'] = comment.user.username
		comment_serialize['current_user'] = request.user.username

		Comments.objects.get(id=kwargs.get('comment_id')).delete()

		return JsonResponse(comment_serialize,safe=False)


class ViewPost(DetailView):
	"""
	View Post
	"""

	model = Feeds
	template_name = "feed/feed_view.html"

	def get_context_data(self,**kwargs):
		context = super(ViewPost,self).get_context_data(**kwargs)
		context['comment_data'] = Comments.objects.filter(post_id=context.get('feeds').id)
		context['comment_form'] = CommentForm()
		context['search_form'] = SearchForm()
		context['user_data'] = self.request.user
		context['current_user'] = self.request.user

		return context


		








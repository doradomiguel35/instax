from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView,View
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from accounts.models import Account,Followers
from user_profile.models import PicturesUser
from feed.models import Feeds
from accounts.serializers import FollowerSerializer
from feed.serializers import FeedSerialize
from .serializers import UserSerialize,ProfPicSerialize
from feed.forms import SearchForm
from .forms import EditProfileForm,ProfPicForm
from django.contrib.auth import logout
from accounts.views import LoginView


class ProfileView(TemplateView):
	"""
	Profile View
	GET - get number of followers,profile pic, search form etch.
	POST - follow/unfollow user

	"""
	
	template_name = 'user_profile/profile.html'

	followers = Followers.objects.all()
	
	def get(self,request,*args,**kwargs):
		username = kwargs.get('username')

		current_user = self.request.user
		
		account = User.objects.get(username=username)
		
		pictures = PicturesUser.objects.filter(user_id=account.id)
		
		search_form = SearchForm()

		try:
			followed = Followers.objects.values(
				'followed_user__username',
				'follower_username',
				'follow'
		
			).get(
		
				followed_user__username=account.username,
				follower_username=self.request.user.username
			)
		
		except:
		
			followed = False

		try: 	
			package = {
				'user_data':account,
				'followers':self.followers,
				'no_prof_pic':False,
				'pictures':pictures,
				'search_form':search_form,
				'current_user':current_user,
				'followed': followed,
			}
			
			return render(
				request,
				self.template_name,
				package
			)

		except:
			package = {
				'user_data': account,
				'followers':self.followers,
				'no_prof_pic':True,
				'pictures':pictures,
				'search_form':search_form,
				'current_user': current_user,
				'followed':followed,
			}
			
			return render(
				request,
				self.template_name,
				package
			)


	def post(self,request,*args,**kwargs):
		user = User.objects.get(username=kwargs.get('username'))
		following_user = Account.objects.get(user_id=request.user.id)
		follow_account = Account.objects.get(user_id=user.id)
		
		try:
			account_follow =  Followers.objects.values(
				'followed_user__username',
				'follower_username',
				'follow'
			).get(
				followed_user__username=user.username,
				follower_username=self.request.user.username
			)

			if account_follow.get('follow') == True:
				follow_account.followers-=1
				following_user.following-=1

				unfollow = Followers.objects.get(followed_user_id=user.id)
				unfollow.follow = False

				unfollow.save()
				follow_account.save()
				following_user.save()
				
				data = {
					'follow':unfollow.follow,
					'followers': follow_account.followers
					}
				
				return JsonResponse(data, safe=False)

			else:
				follow_account.followers+=1
				following_user.following+=1

				follow = Followers.objects.get(followed_user_id=user.id)
				follow.follow = True
				follow_account.save()
				follow.save()
				following_user.save()
				
				data = {
					'follow':follow.follow,
					'followers': follow_account.followers
					}
				
				return JsonResponse(data, safe=False)
			
		except:
			follow_account.followers+=1
			following_user.following+=1

			follow = Followers(
				followed_user_id=user.id,
				follower_username=self.request.user,
				follow=True
			)

			follow.save()
			follow_account.save()
			following_user.save()
			
			data = {
					'follow':follow.follow,
					'followers': follow_account.followers
					}
				
			return JsonResponse(data, safe=False)


class UserProfileView(TemplateView):
	"""
	View User Profile
	"""

	template_name = 'user_profile/profile.html'

	followers = Followers.objects.all()
	
	def get(self,request,*args,**kwargs):

		current_user = self.request.user
		
		account = User.objects.get(username=request.user.username)
		
		pictures = PicturesUser.objects.filter(user_id=account.id)
		
		search_form = SearchForm()

		try:
			followed = Followers.objects.values(
				'followed_user__username',
				'follower_username',
				'follow'
		
			).get(
		
				followed_user__username=account.username,
				follower_username=self.request.user.username
			)
		
		except:
			followed = False

		
		try: 	
			package = {
				'user_data':account,
				'followers':self.followers,
				'no_prof_pic':False,
				'pictures':pictures,
				'search_form':search_form,
				'current_user':current_user,
				'followed': followed,
			}
			
			return render(
				request,
				self.template_name,
				package
			)

		except:
			package = {
				'user_data': account,
				'followers':self.followers,
				'no_prof_pic':True,
				'pictures':pictures,
				'search_form':search_form,
				'current_user': current_user,
				'followed':followed,
			}
			
			return render(
				request,
				self.template_name,
				package
			)


class EditProfile(TemplateView):
	"""
	Edit profile

	"""
	template_name = "user_profile/edit_profile.html"
	
	def get(self,request,*args,**kwargs):
		search_form = SearchForm()
		edit_form = EditProfileForm(instance=request.user)
		change_password_form = PasswordChangeForm(user=request.user)
		account = Account.objects.get(user_id=request.user.id)
		archived_post = Feeds.objects.filter(user_id=self.request.user.id,archived=True)
		prof_pic_form = ProfPicForm()

		try:
			account.prof_pic.url
			prof_pic = account.prof_pic.url
		except:
			prof_pic = False

		package = {
			'account_user':account,
			'current_user':request.user,
			'search_form':search_form,
			'edit_form': edit_form,
			'prof_pic_form':prof_pic_form,
			'archived_post':archived_post,	
			'change_password_form':change_password_form,
			'prof_pic':prof_pic,
		}
		
		return render(request,self.template_name,package)

	def post(self,request,*args,**kwargs):
		user = User.objects.get(username=request.user.username)
		account_user = Account.objects.get(user_id=request.user.id)
		search_form = SearchForm()
		edit = EditProfileForm(request.POST,instance=request.user)
		prof_pic_form = ProfPicForm(data=request.POST,files=request.FILES,instance=account_user)
		
		try:
			account.prof_pic.url
			prof_pic = account.prof_pic.url
		except:
			prof_pic = False

		if edit.is_valid() and prof_pic_form.is_valid():
			edit.save()
			prof_pic_form.save()
			serialize_edit = UserSerialize(User.objects.get(username=request.user.username))
			serialize_pic = ProfPicSerialize(Account.objects.get(user_id=request.user.id))
			data = {
				'profile': serialize_edit.data,
				'prof_account': serialize_pic.data
			}

			return JsonResponse(data, safe=False)

		else:
			return JsonResponse({'errors':edit.errors},safe=False)


class ChangePassword(View):
	"""
	Change Password

	"""
	template_name = "user_profile/edit_profile.html"
	
	def post(self,request,*args,**kwargs):
		search_form = SearchForm()
		edit_form = EditProfileForm(instance=request.user)
		change_password_form = PasswordChangeForm(user=request.user)
		account = Account.objects.get(user_id=request.user.id)
		prof_pic_form = ProfPicForm()
		
		password_form = PasswordChangeForm(data=request.POST,user=request.user)

		try:
			account.prof_pic.url
			prof_pic = account.prof_pic.url
		except:
			prof_pic = False

		package = {
			'account_user':account,
			'current_user':request.user,
			'search_form':search_form,
			'edit_form': edit_form,
			'change_password_form': password_form,
			'prof_pic_form':prof_pic_form,
			'prof_pic':prof_pic,
		}

		if password_form.is_valid():
			password_form.save()
			update_session_auth_hash(request,password_form.user)
			print('if')
			package['success'] = "New Password Set"
			return render(request,self.template_name,package)


		else:
			print('else')
			package['errors'] = password_form.errors
			package['pic_errors'] = prof_pic_form.errors
			return render(request,self.template_name,package)


class DeletePost(View):
	"""
	Delete Post
	POST - delete post completely from archive
	
	"""

	def post(self,request,*args,**kwargs):
		feed = Feeds.objects.get(id=kwargs.get('feed_id'))
		feed_serialize = FeedSerialize(feed)
		serialized = feed_serialize.data
		PicturesUser.objects.get(id=feed.images.id).delete()
		return JsonResponse({'data': serialized},safe=False)


class UnarchivePost(View):
	"""
	Unarchive Post
	POST - remove post from archive, restore it to feeds
	"""

	def post(self,request,*args,**kwargs):
		feed = Feeds.objects.get(id=kwargs.get('feed_id'))
		feed.archived= False;
		feed.save()
		feed_serialize = FeedSerialize(feed)
		serialized = feed_serialize.data
		return JsonResponse({'data':serialized},safe=False)


class Logout(TemplateView):
	"""
	Logout the user
	GET - log out current user, redirect to login page
	"""
	
	template_name = 'accounts/login/login.html'

	def get(self,request,*args,**kwargs):
		logout(request)
		return HttpResponseRedirect(reverse('account:login'))










		




		



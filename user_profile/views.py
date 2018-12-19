from django.shortcuts import render
from django.views.generic import TemplateView
from django.core import serializers
from django.http import JsonResponse
from accounts.models import Account,Followers
from user_profile.models import PicturesUser
from django.contrib.auth.models import User
from accounts.serializers import FollowerSerializer
from .serializers import UserSerialize,ProfPicSerialize
from feed.forms import SearchForm
from .forms import EditProfileForm,ProfPicForm

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
				print('if')
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
				print('else')
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
			print('except')
			follow = Followers(followed_user_id=user.id,follower_username=self.request.user,follow=True)
			follow.save()
			follow_account.save()
			following_user.save()
			
			data = {
					'follow':follow.follow,
					'followers': follow_account.followers
					}
				
			return JsonResponse(data, safe=False)


class EditProfile(TemplateView):
	"""
	Edit profile

	"""
	template_name = "user_profile/edit_profile.html"
	
	def get(self,request,*args,**kwargs):
		search_form = SearchForm()
		edit_form = EditProfileForm(instance=request.user)
		account = Account.objects.get(user_id=request.user.id)
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
			'prof_pic':prof_pic,
		}

		return render(request,self.template_name,package)

	def post(self,request,*args,**kwargs):
		user = User.objects.get(username=request.user.username)
		account_user = Account.objects.get(user_id=request.user.id)

		edit = EditProfileForm(request.POST,instance=request.user)
		prof_pic = ProfPicForm(data=request.POST,files=request.FILES,instance=account_user)
		
		if edit.is_valid() and prof_pic.is_valid():
			edit.save()
			prof_pic.save()
			serialize_edit =UserSerialize(User.objects.get(username=request.user.username))
			serialize_pic = ProfPicSerialize(Account.objects.get(user_id=request.user.id))
			data = {
				'profile': serialize_edit.data,
				'prof_account': serialize_pic.data
			}
			
			return JsonResponse(data, safe=False)

		package = {
			'account_user':account,
			'current_user':request.user,
			'search_form':search_form,
			'edit_form': edit_form,
			'prof_pic_form':prof_pic_form,
			'prof_pic':prof_pic,
		}
		return render(request,self.template_name,package)

		




		



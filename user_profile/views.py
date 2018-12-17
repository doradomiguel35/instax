from django.shortcuts import render
from django.views.generic import TemplateView
from django.core import serializers
from django.http import JsonResponse
from accounts.models import Account,Followers
from user_profile.models import PicturesUser
from django.contrib.auth.models import User
from accounts.serializers import FollowerSerializer
from feed.forms import SearchForm

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
			print('try user')
			return render(request,self.template_name,{
				'user_data':account,
				'followers':self.followers,
				'no_prof_pic':False,
				'pictures':pictures,
				'search_form':search_form,
				'current_user':current_user,
				'followed': followed,
			})

		except:
			print('except user')
			return render(request,self.template_name,{
				'user_data': account,
				'followers':self.followers,
				'no_prof_pic':True,
				'pictures':pictures,
				'search_form':search_form,
				'current_user': current_user,
				'followed':followed,
			})	

	def post(self,request,*args,**kwargs):
		user = User.objects.get(username=kwargs.get('username'))
		
		try:
			account_follow =  Followers.objects.values(
				'followed_user__username',
				'follower_username',
				'follow'
			).get(
				followed_user__username=user.username,
				follower_username=self.request.user.username
			)

			follow_account = Account.objects.get(user_id=user.id)
			if account_follow.get('follow') == True:
				follow_account.followers-=1
				unfollow = Followers.objects.get(followed_user_id=user.id)
				unfollow.follow = False
				unfollow.save()
				follow_account.save()
				print('if')
				data = {
					'follow':unfollow.follow,
					'followers': follow_account.followers
					}
				return JsonResponse(data, safe=False)

			else:
				follow_account.followers+=1
				follow = Followers.objects.get(followed_user_id=user.id)
				follow.follow = True
				follow_account.save()
				follow.save()
				print('else')
				data = {
					'follow':follow.follow,
					'followers': follow_account.followers
					}
				return JsonResponse(data, safe=False)
			
		except:
			follow_account = Account.objects.get(user_id=user.id)
			follow_account.followers+=1
			follow = Followers(followed_user_id=user.id,follower_username=self.request.user,follow=True)
			follow.save()
			follow_account.save()
			print('except')
			data = {
					'follow':follow.follow,
					'followers': follow_account.followers
					}
				
			return JsonResponse(data, safe=False)

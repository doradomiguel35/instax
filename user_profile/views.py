from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import Account,Followers
from user_profile.models import PicturesUser
from django.contrib.auth.models import User

class ProfileView(TemplateView):
	"""
	Profile View

	"""
	template_name = 'user_profile/profile.html'
	followers = Followers.objects.all()
	
	def get(self,request,*args,**kwargs):
		username = kwargs.get('username')
		
		account = User.objects.get(username=username)
		pictures = PicturesUser.objects.filter(user_id=account.id)
		try: 	
			account.account.prof_pic.url

			return render(request,self.template_name,{
				'user_data': account,
				'followers':self.followers,
				'no_prof_pic': False,
				'pictures':pictures
			})
			
		except:
			return render(request,self.template_name,{
				'user_data': account,
				'followers':self.followers,
				'no_prof_pic': True,
				'pictures':pictures
			})				

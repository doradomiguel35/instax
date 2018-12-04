from django.shortcuts import render
from django.views.generic import View
from accounts.models import AccountsModel,FollowersModel
from user_profile.models import PicturesUser

class ProfileView(View):
	template_name = 'user_profile/profile.html'
	followers = FollowersModel.objects.all()
	
	def get(self,request,*args,**kwargs):
		username = kwargs.get('username')
		account = AccountsModel.objects.filter(username=username)
		pictures = PicturesUser.objects.filter(username_id=account[0].id)
		for pic in account:
			try: 	
				pic.prof_pic.url
				return render(request,self.template_name,{'account': account,'followers':self.followers,'no_prof_pic': False,'pictures':pictures})
			except:
				return render(request,self.template_name,{'account': account,'followers':self.followers,'no_prof_pic': True,'pictures':pictures})				

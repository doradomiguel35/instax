from django.shortcuts import render
from django.views.generic import View
from accounts.models import AccountsModel,FollowersModel
from user_profile.models import PicturesUser

class ProfileView(View):
	template_name = 'user_profile/profile.html'

	account = AccountsModel.objects.filter(username='marvelousfaisan35')
	pictures = PicturesUser.objects.filter(username_id=account[0].id)
	followers = FollowersModel.objects.all()

	import pdb;pdb.set_trace()

	def get(self,request,*args,**kwargs):
		for pic in self.account:
			try: 
				pic.prof_pic.url
				return render(request,self.template_name,{'account': self.account,'followers':self.followers,'no_prof_pic': False,'pictures':self.pictures})
			except:
				return render(request,self.template_name,{'account': self.account,'followers':self.followers,'no_prof_pic': True,'pictures':self.pictures})				

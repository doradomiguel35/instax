from django.shortcuts import render
from django.views.generic import View
from accounts.models import AccountsModel,FollowersModel


class ProfileView(View):
	template_name = 'user_profile/profile.html'

	account = AccountsModel.objects.filter(username='marvelousfaisan35')
	followers = FollowersModel.objects.all()

	def get(self,request,*args,**kwargs):
		for pic in self.account:
			try: 
				pic.prof_pic.url
				return render(request,self.template_name,{'account': self.account,'followers':self.followers,'no_prof_pic': False})
			except:
				return render(request,self.template_name,{'account': self.account,'followers':self.followers,'no_prof_pic': True,})				

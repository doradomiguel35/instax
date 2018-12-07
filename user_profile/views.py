from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import AccountsModel,FollowersModel
from user_profile.models import PicturesUser

class ProfileView(TemplateView):
	"""
	Profile View

	"""
	template_name = 'user_profile/profile.html'
	followers = FollowersModel.objects.all()
	
	def get(self,request,*args,**kwargs):
		username = kwargs.get('username')
		account = AccountsModel.objects.get(username=username)
		pictures = PicturesUser.objects.filter(username_id=account.id)
		try: 	
			account.prof_pic.url
			return render(request,self.template_name,{'user_data': account,'followers':self.followers,'no_prof_pic': False,'pictures':pictures})
		except:
			return render(request,self.template_name,{'user_data': account,'followers':self.followers,'no_prof_pic': True,'picture':pictures})				

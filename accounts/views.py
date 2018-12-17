from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import RegisterValidation,LoginValidation
from .models import Account
from feed.models import Feeds,Comments,LikesUser
from django.views.generic import TemplateView
from feed.forms import CommentForm,FeedForm
from user_profile.forms import PicturesForm
from feed.forms import SearchForm

# Create your views here.
class RegisterView(TemplateView):
	"""
	Register View
	
	"""

	template_name = 'accounts/register/register.html'
	context = User.objects.all()
	feed_data = Feeds.objects.all().order_by('-id')
	comment_data = Comments.objects.all()
	get_forms = RegisterValidation()
	comment_form = CommentForm()
	feed_form = FeedForm()
	picture_form = PicturesForm()
	search_form = SearchForm()
	
	def get(self, *args, **kwargs):
		return render(self.request,self.template_name, {
			'context_data': self.context,
			'forms':self.get_forms})

	def post(self,request, *args, **kwargs):
		form = RegisterValidation(request.POST)
		if form.is_valid():
			user = form.save()
			user.set_password(form.cleaned_data.get('password'))
			user.save()
			user = authenticate(username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))
			login(request,user)
			return render(request,'feed/feed_user.html',{
				'feed_data':self.feed_data,
				'comment_data':self.comment_data,
				'user_data':self.request.user,
				'comment_form':self.comment_form,
				'feed_form':self.feed_form,
				'picture_form':self.picture_form,
				'search_form':self.search_form,
				'current_user':self.request.user
			})

		return render(request,self.template_name,{'forms':form}) 


class LoginView(TemplateView):
	"""
	Login View

	"""

	template_name = 'accounts/login/login.html'
	feed_data = Feeds.objects.all().order_by('-id')
	comment_data = Comments.objects.all()
	get_forms = LoginValidation()
	comment_form = CommentForm()
	feed_form = FeedForm()
	picture_form = PicturesForm()	
	search_form = SearchForm()
	
	def get(self,*args,**kwargs):
		return render(self.request, self.template_name,{'forms':self.get_forms})

	def post(self,request, *args, **kwargs):
		forms = LoginValidation(self.request.POST)
		if forms.is_valid():
			user = authenticate(username=forms.cleaned_data.get('username'),password=forms.cleaned_data.get('password'))
			login(request,user)
			return render(request,'feed/users_page.html',{
				'feed_data':self.feed_data,
				'comment_data':self.comment_data,
				'forms':forms,
				'user_data': self.request.user,
				'comment_form':self.comment_form,
				'feed_form':self.feed_form,
				'picture_form':self.picture_form,
				'search_form':self.search_form,
				'current_user':self.request.user
			})
		return render(request, self.template_name,{'forms':forms })

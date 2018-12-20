from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import RegisterValidation,LoginValidation
from .models import Account,Followers
from feed.models import Feeds,Comments,LikesUser
from django.views.generic import TemplateView
from feed.forms import CommentForm,FeedForm
from user_profile.forms import PicturesForm
from feed.forms import SearchForm

# Create your views here.
class RegisterView(TemplateView):
	"""
	Register View
	GET - get forms and render template
	POST - register user account, get user information
	"""

	template_name = 'accounts/register/register.html'
	context = User.objects.all()
	
	get_forms = RegisterValidation()
	comment_form = CommentForm()
	feed_form = FeedForm()
	picture_form = PicturesForm()
	search_form = SearchForm()
	
	def get(self, *args, **kwargs):
			
		return render(
			self.request,
			self.template_name, 
			{
				'context_data': self.context,
				'forms':self.get_forms
			}
		)

	def post(self,request, *args, **kwargs):
		
		form = RegisterValidation(request.POST)
		
		if form.is_valid():
			user = form.save()
			user.set_password(form.cleaned_data.get('password'))
			user.save()
			account = Account(user_id=user.id)
			account.save()

			user = authenticate(
					username=form.cleaned_data.get('username'),
					password=form.cleaned_data.get('password')
			)

			login(request,user)
			
			followers = Followers.objects.filter(follow=True,follower_username=request.user.username).values('followed_user_id')
		
			feed_data = Feeds.objects.filter(user_id__in=followers) | Feeds.objects.filter(user_id=request.user.id)
			
			comment_data = Comments.objects.filter(post_id__in=feed_data.values('id'))
			
			feed_data._result_cache = None
		
			comment_data._result_cache = None


			package = {
				'feed_data':feed_data.order_by('-id'),
				'comment_data':comment_data,
				'user_data':request.user,
				'comment_form':self.comment_form,
				'feed_form':self.feed_form,
				'picture_form':self.picture_form,
				'search_form':self.search_form,
				'current_user':self.request.user
			}

		
			return render(request,'feed/users_page.html',package)

		return render(request,self.template_name,{'forms':form}) 


class LoginView(TemplateView):
	"""
	Login View

	"""

	template_name = 'accounts/login/login.html'
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
			
			followers = Followers.objects.filter(follow=True,follower_username=request.user.username).values('followed_user_id')
		
			feed_data = Feeds.objects.filter(user_id__in=followers) | Feeds.objects.filter(user_id=request.user.id)
			
			comment_data = Comments.objects.filter(post_id__in=feed_data.values('id'))
	
			package = {
				'feed_data':feed_data,
				'comment_data':comment_data,
				'forms':forms,
				'user_data': request.user,
				'comment_form':self.comment_form,
				'feed_form':self.feed_form,
				'picture_form':self.picture_form,
				'search_form':self.search_form,
				'current_user':request.user
			}

			return render(
				request,
				'feed/users_page.html',
				package
			)
		
		return render(
			request, 
			self.template_name,
			{'forms':forms }
		)

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
	# path('create/',views.create_post,name='create_post')
]
from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
	path('<str:username>',views.ProfileView.as_view(),name="profile"),
	path('follow/<str:username>',views.ProfileView.as_view(),name="follow")
]
from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
	path('<str:username>',views.ProfileView.as_view(),name="profile"),
	path('follow/<str:username>',views.ProfileView.as_view(),name="follow"),
	path('edit_profile/',views.EditProfile.as_view(),name="edit"),
	path('change_password/',views.ChangePassword.as_view(),name="change_password"),
	path('delete_post/<int:feed_id>/',views.DeletePost.as_view(),name='delete_post'),	
	path('unarchive_post/<int:feed_id>/',views.UnarchivePost.as_view(),name='unarchive'),
	path('logout/',views.Logout.as_view(),name='logout'),
	path('user/<str:username>',views.UserProfileView.as_view(),name='profile_user')
]
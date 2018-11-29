from django.urls import path
from . import views

urlpatterns = [
	path('', views.FeedsView.as_view(),name='feeds')
]
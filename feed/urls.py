from django.urls import path
from . import views

app_name = 'feeds'

urlpatterns = [
	path('<str:username>', views.FeedsView.as_view(),name='feeds'),
	path('<str:username>/<str:profile>', views.FeedUser.as_view(),name='feeds_profile'),
	path('comment/<int:feed_id>/<str:username>', views.FeedsView.as_view(),name='feeds_comment')
]
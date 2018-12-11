from django.urls import path
from . import views

app_name = 'feeds'

urlpatterns = [
    path('',views.FeedsView.as_view(),name='feeds'),
    path('comment/<int:feed_id>/',views.FeedsView.as_view(),name='comment'),
    path('like/<int:feed_id>/',views.LikeView.as_view(),name='like')
]
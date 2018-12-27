from django.urls import path
from . import views

app_name = 'feeds'

urlpatterns = [
    path('',views.FeedsView.as_view(),name='feeds'),
    path('comment/<int:feed_id>/',views.FeedsView.as_view(),name='comment'),
    path('like/<int:feed_id>/',views.LikeView.as_view(),name='like'),
    path('create_post/',views.CreatePost.as_view(),name='create_post'),
    path('search/',views.Search.as_view(),name='search'),
    path('archive/<int:feed_id>',views.ArchivePost.as_view(),name='archive'),
    # path('edit_post/<int:feed_id>',views.)
]
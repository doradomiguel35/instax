from django.urls import path
from . import views

app_name = 'feeds'

urlpatterns = [
    path('',views.FeedsView.as_view(),name='feeds'),
    path('comment/<int:feed_id>/',views.FeedsView.as_view(),name='comment'),
    path('like/<int:feed_id>/',views.LikeView.as_view(),name='like'),
    path('create_post/',views.CreatePost.as_view(),name='create_post'),
    path('search/',views.Search.as_view(),name='search'),
    path('archive/<int:feed_id>/',views.ArchivePost.as_view(),name='archive'),
    path('edit_post/<int:feed_id>/<int:image_id>/',views.EditPost.as_view(),name='edit_post'),
    path('edit_comment/<int:comment_id>/',views.EditComment.as_view(),name='edit_comment'),
    path('get_comment/<int:comment_id>/',views.EditComment.as_view(),name='get_comment'),
    path('delete_comment/<int:comment_id>/',views.DeleteComment.as_view(),name='delete_comment'),
    path('view_post/<int:pk>/',views.ViewPost.as_view(),name='view_post'),

]
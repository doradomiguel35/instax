from django.urls import path
from . import views

app_name = 'feeds'

urlpatterns = [
    path('',views.FeedsView.as_view(),name='feeds'),
    path('comment/<int:feed_id>/',views.FeedsView.as_view(),name='comment'),
]
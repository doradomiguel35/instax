from django.urls import path
from . import views

app_name = 'feeds'

urlpatterns = [
    path('',views.FeedsView.as_view(),name='feeds'),
]
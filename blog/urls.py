from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('', views.button),
    path('', views.home, name='data'),
    path('youtube/', views.youtube, name='youtube-data')
]

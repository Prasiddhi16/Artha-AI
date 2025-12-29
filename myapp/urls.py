from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analytics/',views.analytics,name='analytics'),
    path('review/', views.review, name='review'),
    path('goals/', views.goals, name='goals'),
    path('help/', views.help, name='help'),
]
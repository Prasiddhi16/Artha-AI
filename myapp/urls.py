from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('analytics/',views.analytics,name='analytics'),
    path('review/', views.review, name='review'),
    path('goals/', views.goals, name='goals'),
    path('help/', views.help, name='help'),
    path('profile/', views.profile, name='profile'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('chatbot/', views.chatbot, name='chatbot'),

   

]
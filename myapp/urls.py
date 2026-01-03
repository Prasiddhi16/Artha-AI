from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
<<<<<<< HEAD
    path('analytics/',views.analytics,name='analytics'),
    path('budget/',views.budget,name='budget'),
    path('review/', views.review, name='review'),
    path('goals/', views.goals, name='goals'),
    path('help/', views.help, name='help'),
    path('profile/', views.profile, name='profile'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
=======
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('goals/', views.goals, name='goals'),
    path('analytics/', views.analytics, name='analytics'),
    path('review/', views.review, name='review'),
   path('help/', views.help_view, name='help'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
>>>>>>> 9c8d4100f4f95d2b0f7195d4857afe1ef3a16c90
    path('chatbot/', views.chatbot, name='chatbot'),
]
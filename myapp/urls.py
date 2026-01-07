from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('goals/', views.goals, name='goals'),
    path('analytics/', views.analytics, name='analytics'),
    path('budget/',views.budget,name='budget'),
    path('review/', views.review, name='review'),
    path('help/', views.help_view, name='help'),
    path('profile/', views.profile, name='profile'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('api/weekly_summary/',views.weekly_summary_api,name='weekly_summary_api'),
    path('api/monthly_category/',views.monthly_category_api,name='monthly_category_api'),
    path('api/category_trend/', views.category_trend_api, name='category_trend_api'),

]
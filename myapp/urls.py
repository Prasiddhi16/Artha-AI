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
    path('goal/<int:goal_id>/contribute/', views.add_contribution, name='add_contribution'),
    path('analytics/', views.analytics, name='analytics'),
    path('budget/',views.budget,name='budget'),
    path('review/', views.review, name='review'),
    path('help/', views.help_view, name='help'),
    path('profile/', views.profile, name='profile'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('ajax/add_contribution/', views.add_contribution_ajax, name='add_contribution_ajax'),
    path('delete_goal/', views.delete_goal, name='delete_goal'),
    path("goals/contributions/",views.goal_contributions_ajax,name="goal_contributions_ajax"),


    path("scan-receipt/", views.scan_receipt, name="scan_receipt"),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),

]
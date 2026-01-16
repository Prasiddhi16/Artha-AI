from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('goals/', views.goals, name='goals'),
    path('goal/<int:goal_id>/contribute/', views.add_contribution, name='add_contribution'),
    path('analytics/', views.analytics, name='analytics'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
<<<<<<< HEAD
=======
=======

    # Auth
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),

    # Password / Email
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify-email/', views.verify_email, name='verify_email'),

    # App pages
>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba
    path('goals/', views.goals, name='goals'),
    path('goal/<int:goal_id>/contribute/', views.add_contribution, name='add_contribution'),
    path('analytics/', views.analytics, name='analytics'),
    path('review/', views.review, name='review'),
<<<<<<< HEAD
=======
<<<<<<< HEAD
    path('utilities/',views.utilities,name='utilities'),
=======
    path('utilities/', views.utilities, name='utilities'),
>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba
    path('budget/', views.budget_view, name='budget'),
    path('help/', views.help_view, name='help'),
    path('profile/', views.profile, name='profile'),
    path('chatbot/', views.chatbot, name='chatbot'),
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba
    path('api/weekly_summary/',views.weekly_summary_api,name='weekly_summary_api'),
    path('api/monthly_category/',views.monthly_category_api,name='monthly_category_api'),
    path('api/category_trend/', views.category_trend_api, name='category_trend_api'),
    path('ajax/add_contribution/', views.add_contribution_ajax, name='add_contribution_ajax'),
    path('delete_goal/', views.delete_goal, name='delete_goal'),
    path("goals/contributions/",views.goal_contributions_ajax,name="goal_contributions_ajax"),
    path("delete-transaction/", views.delete_transaction, name="delete_transaction"),
    path("scan-receipt/", views.scan_receipt, name="scan_receipt"),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path("filter-transactions/", views.filter_transactions, name="filter_transactions"),
<<<<<<< HEAD
    path("delete-transaction-home/", views.delete_transactionhome, name="delete_transactionhome"),
    path('edit_budget/', views.edit_budget, name='edit_budget'),
    path('delete_money_flow/', views.delete_money_flow, name='delete_money_flow'),
    path('delete_budget/', views.delete_budget, name='delete_budget'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/notifications/', views.update_notifications, name='update_notifications'),
    path('profile/password/', views.update_password, name='update_password'),
    path('profile/privacy/', views.update_privacy_settings, name='update_privacy_settings'),
    path('profile/two-factor/', views.toggle_two_factor, name='toggle_two_factor'),
    path('profile/delete/', views.delete_account, name='delete_account'),

]
=======
     path("delete-transaction-home/", views.delete_transactionhome, name="delete_transactionhome"),
    path('ajax/add_contribution/', views.add_contribution_ajax, name='add_contribution_ajax'),
    path('delete_goal/', views.delete_goal, name='delete_goal'),
    path("goals/contributions/",views.goal_contributions_ajax,name="goal_contributions_ajax"),
    path("scan-receipt/", views.scan_receipt, name="scan_receipt"),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),

]
=======

    # APIs / AJAX
    path('api/weekly_summary/', views.weekly_summary_api, name='weekly_summary_api'),
    path('api/monthly_category/', views.monthly_category_api, name='monthly_category_api'),
    path('api/category_trend/', views.category_trend_api, name='category_trend_api'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('ajax/add_contribution/', views.add_contribution_ajax, name='add_contribution_ajax'),
    path('goals/contributions/', views.goal_contributions_ajax, name='goal_contributions_ajax'),
    path('delete_goal/', views.delete_goal, name='delete_goal'),
    path('delete-transaction/', views.delete_transaction, name='delete_transaction'),
    path('delete-transaction-home/', views.delete_transactionhome, name='delete_transactionhome'),
    path('scan-receipt/', views.scan_receipt, name='scan_receipt'),
    path('filter-transactions/', views.filter_transactions, name='filter_transactions'),
    path('set-password/', views.set_password, name='set_password'),

]
>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba

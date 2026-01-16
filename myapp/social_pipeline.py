from django.contrib import messages

def google_signup_message(strategy, details, user=None, is_new=False, *args, **kwargs):
    if is_new:
        request = strategy.request
        messages.success(
            request,
            "Your account has been created. Now you can sign in."
        )
from django.shortcuts import redirect
from django.urls import reverse

def redirect_to_set_password(strategy, user=None, is_new=False, *args, **kwargs):
    if is_new:
        return redirect(reverse('set_password'))

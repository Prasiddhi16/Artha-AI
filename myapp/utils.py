import random

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

# utils.py
import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email, otp):
    send_mail(
        subject="Your Email Verification OTP",
        message=f"Your OTP is {otp}",
        from_email=None,
        recipient_list=[email],
    )

from .models import NotificationEvent

def create_notification(user, message, notification_type="info"):
    """
    Creates a DB-backed notification.
    Overlay will fetch this via AJAX.
    """
    return NotificationEvent.objects.create(
        user=user,
        message=message,
        notification_type=notification_type
    )

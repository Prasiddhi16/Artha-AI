<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba
import random

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP
<<<<<<< HEAD
=======
=======
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
>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba

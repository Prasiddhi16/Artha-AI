from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=50) # Income or Expense
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name or "", **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_email_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    AUTH_PROVIDERS = (
        ('email', 'Email'),
        ('google', 'Google'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)

    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDERS,
        default='email'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image=models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']


    def __str__(self):
        return self.email

# ---------------- Expense Model ----------------
class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - Expense: {self.amount}"

# ---------------- Income Model ----------------
class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - Income: {self.amount}"

# ---------------- Goal Model ----------------
class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    target_date = models.DateField()
    created = models.DateField(auto_now_add=True)

    

    def __str__(self):
        return f"{self.user.email} - Goal: {self.title}"
     # ---------------- GoalContribution Model ----------------

class GoalContribution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.goal.title} contribution: {self.amount}"

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
    
# ---------------- Budget Model ----------------
class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.CharField(max_length=50, blank=True, null=True)

    month = models.IntegerField(null=True,blank=True)  # 1-12
    year = models.IntegerField(null=True, blank=True)   # 2026

    class Meta:
        unique_together = ('user', 'category', 'month', 'year')

    def __str__(self):
        return f"{self.category} - {self.month}/{self.year}: {self.amount}"

# ---------------- Money Flow Model ----------------
class MoneyFlow(models.Model):
    FLOW_TYPES = (
        ('topay', 'You owe'),
        ('toreceive', 'Owed to you'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    flow_type = models.CharField(max_length=10, choices=FLOW_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person_name} - {self.flow_type}: {self.amount}"


# profile models


class Notification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_settings')
    email_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    monthly_reports = models.BooleanField(default=False)
    budget_alerts = models.BooleanField(default=False)
    goal_reminders = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s notifications"

class PrivacySettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='privacy_settings')
    analytics_tracking = models.BooleanField(default=False)
    crash_reporting = models.BooleanField(default=False)
    usage_data = models.BooleanField(default=False)
    spending_insights = models.BooleanField(default=False)
    two_factor_auth = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s privacy settings"

class EmailOTP(models.Model):
    PURPOSE_CHOICES = (
        ("signup", "Signup"),
        ('change_email', 'Change Email'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_otps',  null=True,
        blank=True)
    email = models.EmailField( null=True, blank=True)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES,  null=True, blank=True  )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.email} | {self.purpose}"

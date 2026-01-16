from django import forms
from myapp.models import User
from django import forms
from .models import Goal, GoalContribution 
from .models import Budget, MoneyFlow
<<<<<<< HEAD
from .models import Notification, PrivacySettings
from django.contrib.auth.forms import PasswordChangeForm

=======

<<<<<<< HEAD
=======
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
<<<<<<< HEAD
        fields = ['name', 'email', 'password']
=======
<<<<<<< HEAD
        fields = ['name', 'email', 'password']
=======
        fields = ['name', 'email']
>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
<<<<<<< HEAD
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
=======
<<<<<<< HEAD
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
=======

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False  # 🔐 inactive until email OTP verification
        if commit:
            user.save()
        return user

>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba
    
from django.contrib.auth import get_user_model
from .models import Goal, GoalContribution

User = get_user_model()


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'target_amount', 'category', 'target_date']


class GoalContributionForm(forms.ModelForm):
    class Meta:
        model = GoalContribution
        fields = ['goal', 'amount', 'date', 'note']
        widgets = {
            'goal': forms.HiddenInput()  # The goal ID is passed from frontend
        }
  

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your registered email")


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category','icon', 'amount', 'month', 'year']

<<<<<<< HEAD
        def clean_amount(self):
            amount = self.cleaned_data.get('amount')

            if amount is None:
                raise forms.ValidationError("Amount is required.")

            if amount <= 0:
                raise forms.ValidationError("Budget must be greater than zero.")

            return amount

=======
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba
class MoneyFlowForm(forms.ModelForm):
    class Meta:
        model = MoneyFlow
        fields = ['person_name', 'amount', 'flow_type']

<<<<<<< HEAD
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone']

        def clean_name(self):
            name = self.cleaned_data["name"]
            if len(name) < 2:
                raise forms.ValidationError("Name is too short.")
            return name

class NotificationForm(forms.ModelForm):
    class Meta:
        model= Notification
        fields=['email_notifications','push_notifications','monthly_reports','budget_alerts','goal_reminders']


class PasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = PrivacySettings
        fields = ['analytics_tracking', 'crash_reporting', 'usage_data', 
                  'spending_insights', 'two_factor_auth']


=======
>>>>>>> ca6b7c55dbc386a851d5016eb536c9b23cd699ba

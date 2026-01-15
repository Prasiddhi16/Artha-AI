from django import forms
from myapp.models import User
from django import forms
from .models import Goal, GoalContribution 
from .models import Budget, MoneyFlow

<<<<<<< HEAD
=======
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
<<<<<<< HEAD
        fields = ['name', 'email', 'password']
=======
        fields = ['name', 'email']
>>>>>>> 8146b54 (Initial commit of AI-Artha1 Django project)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
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

class MoneyFlowForm(forms.ModelForm):
    class Meta:
        model = MoneyFlow
        fields = ['person_name', 'amount', 'flow_type']


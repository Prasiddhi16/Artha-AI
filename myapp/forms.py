from django import forms
<<<<<<< HEAD
from myapp.models import User
from django import forms
from .models import Goal, GoalContribution 

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
=======
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


>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'target_amount', 'category', 'target_date']

<<<<<<< HEAD
=======

>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
class GoalContributionForm(forms.ModelForm):
    class Meta:
        model = GoalContribution
        fields = ['goal', 'amount', 'date', 'note']
        widgets = {
<<<<<<< HEAD
            'goal': forms.HiddenInput()  # The goal ID is passed from frontend
        }
  
=======
            'goal': forms.HiddenInput()
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
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310

from django import forms
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
  
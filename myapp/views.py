from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
import random, time
from django.db.models import Sum

from .models import User, Expense, Income, Goal
from .forms import SignUpForm
from .models import GoalContribution
from django.shortcuts import render, redirect, get_object_or_404



# ---------------- Signup ----------------
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully! You can now sign in.")
            return redirect('signin')
        else:
            messages.error(request, "Please fix the errors below")
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

# ---------------- Signin ----------------
def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'myapp/signin.html')

# ---------------- Logout ----------------
def logout_view(request):
    logout(request)
    return redirect('signin')

def chatbot(request):
    return render(request, 'myapp/chatbot.html')

# ---------------- Forgot Password ----------------
def forgot_password(request):
    if request.method == "POST":
        messages.success(request, "OTP sent successfully!")
        return redirect('verify_otp')
    return render(request, 'myapp/forgotpassword.html')

# ---------------- Verify OTP ----------------
def verify_otp(request):
    if request.method == "POST":
        messages.success(request, "OTP verified successfully!")
        return redirect('reset_password')
    return render(request, 'myapp/verify_otp.html')

# ---------------- Reset Password ----------------
def reset_password(request):
    if request.method == "POST":
        messages.success(request, "Password reset successfully!")
        return redirect('signin')
    return render(request, 'myapp/reset_password.html')



# ---------------- Home / Dashboard ----------------
@login_required(login_url='signin')
def home(request):
    user = request.user

    # ---------- HANDLE ADD TRANSACTION ----------
    if request.method == "POST":
        try:
            amount = request.POST.get("amount")
            transaction_type = request.POST.get("transaction_type")
            category = request.POST.get("category")
            date = request.POST.get("date") or timezone.now().date()

            if not amount:
                messages.error(request, "Amount is required.")
                return redirect('home')

            amount = Decimal(amount)

            if transaction_type == "expense":
                Expense.objects.create(
                    user=user,
                    amount=amount,
                    category=category,
                    description=category,
                    date=date
                )
                messages.success(request, f"Expense of Rs. {amount} added successfully!")

            elif transaction_type == "income":
                Income.objects.create(
                    user=user,
                    amount=amount,
                    category=category,
                    description=category,
                    date=date
                )
                messages.success(request, f"Income of Rs. {amount} added successfully!")

            return redirect('home')

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('home')

    # ---------- DASHBOARD DATA ----------
    expenses = Expense.objects.filter(user=user).order_by('-date')
    incomes = Income.objects.filter(user=user).order_by('-date')

    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    balance = total_income - total_expense

    # Combine recent transactions
    for i in incomes:
        i.transaction_type = 'Income'
    for e in expenses:
        e.transaction_type = 'Expense'

    transactions = sorted(
        list(incomes) + list(expenses),
        key=lambda x: x.date,
        reverse=True
    )[:10]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'transactions': transactions,
    }

    return render(request, 'myapp/home.html', context)

# ---------------- Goals ----------------
@login_required(login_url='signin')
@login_required(login_url='signin')
def goals(request):
    if request.method == "POST":
        Goal.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            target_amount=request.POST.get("target_amount"),
            category=request.POST.get("category"),
            target_date=request.POST.get("target_date"),
        )
        messages.success(request, "Goal added successfully!")
        return redirect('goals')

    user_goals = Goal.objects.filter(user=request.user)
    return render(request, 'myapp/goals.html', {'user_goals': user_goals})


@login_required(login_url='signin')
def add_contribution(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)

    if request.method == "POST":
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        note = request.POST.get("note")

        if not amount or not date:
            return render(request, "goal_detail.html", {"goal": goal, "error": "Amount and date required."})

        # Convert amount to Decimal
        try:
            amount = Decimal(amount)
        except:
            return render(request, "goal_detail.html", {"goal": goal, "error": "Invalid amount."})

        # Save contribution
        contribution = GoalContribution.objects.create(
            user=request.user,
            goal=goal,
            amount=amount,
            date=date,
            note=note
        )

        # Update Goal
        goal.current_contribution += amount
        goal.last_contribution_date = date
        goal.save()

        return redirect("goals")  # or wherever you want

    return render(request, "goal_detail.html", {"goal": goal})

# ---------------- Static Pages ----------------
def analytics(request): return render(request, 'myapp/analytics.html')
def budget(request):return render(request, 'myapp/budget.html')
def review(request): return render(request, 'myapp/review.html')
def help_view(request): return render(request, 'myapp/help.html')
def profile(request): return render(request, 'myapp/profile.html')
def settings_view(request): return render(request, 'myapp/settings.html')
def chatbot(request): return render(request, 'myapp/chatbot.html')

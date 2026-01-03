from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
import random, time
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import date

from .models import User, Expense, Income, Goal,GoalContribution
from .forms import SignUpForm
from .forms import GoalForm
from .forms import GoalContributionForm
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
def goals(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, "Goal added successfully!")
            return redirect('goals')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GoalForm()

    user_goals = Goal.objects.filter(user=request.user)

    for goal in user_goals:
        total = goal.contributions.aggregate(
            Sum('amount')
        )['amount__sum'] or Decimal('0.00')
        goal.total_contributed = total
        goal.remaining_amount = goal.target_amount - total
        goal.progress_percent = (
            total / goal.target_amount * 100
        ) if goal.target_amount > 0 else 0
        if goal.target_date:
            today = date.today()
            remaining = (goal.target_date - today).days
            goal.days_remaining = remaining if remaining > 0 else 0
        else:
            goal.days_remaining = None


    return render(
        request,
        'myapp/goals.html',
        {
            'user_goals': user_goals,
            'form': form
        }
    )


@login_required(login_url='signin')
def add_contribution(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)

    if request.method == "POST":
        form = GoalContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.user = request.user
            contribution.goal = goal
            contribution.save()

            messages.success(
                request,
                f"₹{contribution.amount} contributed to {goal.title}"
            )
            return redirect('goals')
        else:
            messages.error(request, "Invalid contribution data.")
    else:
        form = GoalContributionForm(initial={'goal': goal})

    return render(
        request,
        'myapp/goal_detail.html',
        {'goal': goal, 'form': form}
    )


from django.http import JsonResponse

@login_required(login_url='signin')
@require_POST
def delete_goal(request):
    goal_id = request.POST.get('goal_id')
    try:
        goal = Goal.objects.get(id=goal_id, user=request.user)
        goal.delete()
        return JsonResponse({"success": True})
    except Goal.DoesNotExist:
        return JsonResponse({"error": "Goal not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@login_required(login_url='signin')
def add_contribution_ajax(request):
    if request.method == "POST":
        goal_id = request.POST.get("goal_id")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        note = request.POST.get("note", "")

        try:
            goal = Goal.objects.get(id=goal_id, user=request.user)
            amount = Decimal(amount)

            contribution = GoalContribution.objects.create(
                user=request.user,
                goal=goal,
                amount=amount,
                date=date,
                note=note
            )

            # Recalculate totals
            total = goal.contributions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            goal_total = total
            progress_percent = (total / goal.target_amount * 100) if goal.target_amount > 0 else 0
            remaining_amount = goal.target_amount - total

            data = {
                "id": goal.id,
                "total_contributed": str(total),
                "progress_percent": round(progress_percent, 1),
                "remaining_amount": str(remaining_amount),
            }

            return JsonResponse(data)

        except Goal.DoesNotExist:
            return JsonResponse({"error": "Goal not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


# ---------------- Static Pages ----------------
def analytics(request): return render(request, 'myapp/analytics.html')
def budget(request):return render(request, 'myapp/budget.html')
def review(request): return render(request, 'myapp/review.html')
def help_view(request): return render(request, 'myapp/help.html')
def profile(request): return render(request, 'myapp/profile.html')
def settings_view(request): return render(request, 'myapp/settings.html')
def chatbot(request): return render(request, 'myapp/chatbot.html')

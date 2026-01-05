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
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import GoalContribution, Goal



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
    icon_map = {
        "First Quarter": "fas fa-seedling",
        "Halfway There": "fas fa-flag",
        "Final Stretch": "fas fa-flag-checkered",
        "Goal Achieved": "fas fa-star"
    }

    for goal in user_goals:
        total = goal.contributions.aggregate(
            Sum('amount')
        )['amount__sum'] or Decimal('0.00')
        goal.total_contributed = total
        goal.remaining_amount = goal.target_amount - total
        goal.progress_percent = min(
    (total / goal.target_amount * 100) if goal.target_amount > 0 else 0,
    100
)

        if goal.target_date:
            today = date.today()
            remaining = (goal.target_date - today).days
            goal.days_remaining = remaining if remaining > 0 else 0
        else:
            goal.days_remaining = None
 # -------- Milestones --------
        milestone_amounts = [0.25, 0.5, 0.75, 1.0]  # 25%, 50%, 75%, 100%
        milestone_names = ["First Quarter", "Halfway There", "Final Stretch", "Goal Achieved"]
        milestones = []
        active_set = False  # Track first active milestone

        for perc, name in zip(milestone_amounts, milestone_names):
            amount = goal.target_amount * Decimal(perc)
            if total >= amount:
                status = "completed"
            elif not active_set:
                status = "active"
                active_set = True
            else:
                status = "upcoming"
                icon_map = {
    "First Quarter": "fas fa-seedling",
    "Halfway There": "fas fa-flag",
    "Final Stretch": "fas fa-flag-checkered",
    "Goal Achieved": "fas fa-star"
}
            milestones.append({
                "name": name,
                 "amount": float(amount),
                "status": status,
                 "icon": icon_map[name]
            })

        goal.dynamic_milestones = milestones

#  Overview calculations   
        
    total_goals = user_goals.count()
    completed_goals = sum(1 for g in user_goals if g.progress_percent >= 100)
    total_target = sum(g.target_amount for g in user_goals) if user_goals else Decimal('0.00')
    total_saved = sum(g.total_contributed for g in user_goals) if user_goals else Decimal('0.00')
    overall_progress = min(
    (total_saved / total_target * 100) if total_target > 0 else 0,
    100
)
    return render(
        request,
        'myapp/goals.html',
        {
            'user_goals': user_goals,
            'form': form,
            'total_goals': total_goals,
            'completed_goals': completed_goals,
            'total_target': total_target,
            'total_saved': total_saved,
            'overall_progress': min(round(overall_progress, 2),100),
        }
    )



@login_required(login_url='signin')
def add_contribution(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)

    if request.method == "POST":
        form = GoalContributionForm(request.POST)

        if form.is_valid():
            contribution = form.save(commit=False)

      
            current_total = goal.contributions.aggregate(
                Sum('amount')
            )['amount__sum'] or Decimal('0.00')

            
            if current_total >= goal.target_amount:
                messages.error(
                    request,
                    "This goal is already completed. No more contributions allowed."
                )
                return redirect('goals')

          
            remaining = goal.target_amount - current_total
            if contribution.amount > remaining:
                contribution.amount = remaining

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

        # Recalculate overview stats
        user_goals = Goal.objects.filter(user=request.user)
        total_goals = user_goals.count()
        completed_goals = sum(1 for g in user_goals if g.contributions.aggregate(Sum('amount'))['amount__sum'] or 0 >= g.target_amount)
        total_target = sum(g.target_amount for g in user_goals) if user_goals else 0
        total_saved = sum(g.contributions.aggregate(Sum('amount'))['amount__sum'] or 0 for g in user_goals) if user_goals else 0
        overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0

        return JsonResponse({
            "success": True,
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "total_target": float(total_target),
            "total_saved": float(total_saved),
            "overall_progress": round(overall_progress, 1)
        })
    except Goal.DoesNotExist:
        return JsonResponse({"error": "Goal not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({"error": str(e)}, status=400)

@login_required(login_url='signin')
@require_POST
def add_contribution_ajax(request):
    goal_id = request.POST.get("goal_id")
    amount = request.POST.get("amount")
    date = request.POST.get("date")
    note = request.POST.get("note", "")

    try:
        goal = Goal.objects.get(id=goal_id, user=request.user)
        amount = Decimal(amount)
        
        # CHECK CURRENT TOTAL
        current_total = goal.contributions.aggregate(
            Sum('amount')
        )['amount__sum'] or Decimal('0.00')

        # BLOCK IF GOAL COMPLETED
        if current_total >= goal.target_amount:
            return JsonResponse({
                "error": "Goal already completed",
                "progress_percent": 100
            }, status=400)

        # PREVENT OVER-CONTRIBUTION
        remaining = goal.target_amount - current_total
        if amount > remaining:
            amount = remaining

        # Save contribution
        contribution = GoalContribution.objects.create(
            user=request.user,
            goal=goal,
            amount=amount,
            date=date,
            note=note
        )

        # Recalculate this goal's totals
        total = goal.contributions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        progress_percent = min(
    round((total / goal.target_amount * 100), 1)
    if goal.target_amount > 0
    else 0,
    100
)
        remaining_amount = goal.target_amount - total
        # Recalculate milestones
        milestone_amounts = [0.25, 0.5, 0.75, 1.0]
        milestone_names = ["First Quarter", "Halfway There", "Final Stretch", "Goal Achieved"]
        milestones = []
        active_set = False
        for perc, name in zip(milestone_amounts, milestone_names):
            amount_m = goal.target_amount * Decimal(perc)
            if total >= amount_m:
                status = "completed"
            elif not active_set:
                status = "active"
                active_set = True
            else:
                status = "upcoming"
            milestones.append({
                "name": name,
                "amount": float(amount_m),
                "status": status
            })
       # ---------- OVERVIEW CALCULATIONS ----------
        user_goals = Goal.objects.filter(user=request.user)

        total_goals = user_goals.count()

        completed_goals = 0
        total_target = Decimal('0.00')
        total_saved = Decimal('0.00')

        for g in user_goals:
            contributed = g.contributions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

            total_target += g.target_amount
            total_saved += contributed

            if contributed >= g.target_amount:
                completed_goals += 1

        overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0


        data = {
           "id": goal.id,
           "title": goal.title,
            "total_contributed": float(total),
            "target_amount": float(goal.target_amount), 
            "progress_percent": min(round(progress_percent, 1),100),
            "remaining_amount": float(remaining_amount),
            "milestones": milestones, 
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "total_target": float(total_target),
            "total_saved": float(total_saved),
            "overall_progress": min(round(overall_progress, 1),100),
        }

        return JsonResponse(data)

    except Goal.DoesNotExist:
        return JsonResponse({"error": "Goal not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

# ---------------- Contribution Ladder ----------------

@login_required
def goal_contributions_ajax(request):
    goal_id = request.GET.get("goal_id")

    if not goal_id:
        return JsonResponse({"error": "Goal ID missing"}, status=400)

    try:
        goal = Goal.objects.get(id=goal_id, user=request.user)
    except Goal.DoesNotExist:
        return JsonResponse({"error": "Goal not found"}, status=404)

    contributions = (
        GoalContribution.objects
        .filter(goal=goal, user=request.user)
        .order_by("date")
    )

    labels = []
    cumulative_amounts = []
    individual_amounts = []
   

    running_total = 0
    for c in contributions:
        running_total += c.amount
        labels.append(c.date.strftime("%Y-%m-%d"))
        cumulative_amounts.append(float(running_total))
        individual_amounts.append(float(c.amount))
        ladder_color = "#28a745" if running_total >= goal.target_amount else "#6d6de0"

    return JsonResponse({
        "goal_title": goal.title,
        "labels": labels,
        "amounts": cumulative_amounts, 
         "individuals": individual_amounts,
              "color": ladder_color 
    })


# ---------------- Static Pages ----------------
def analytics(request): return render(request, 'myapp/analytics.html')
def budget(request):return render(request, 'myapp/budget.html')
def review(request): return render(request, 'myapp/review.html')
def help_view(request): return render(request, 'myapp/help.html')
def profile(request): return render(request, 'myapp/profile.html')
def settings_view(request): return render(request, 'myapp/settings.html')
def chatbot(request): return render(request, 'myapp/chatbot.html')

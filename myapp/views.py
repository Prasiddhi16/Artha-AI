from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
import random, time
<<<<<<< HEAD
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from .models import User, Expense, Income, Goal
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import Max
=======
from django.db.models import Sum, Avg, Max
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot import get_bot_response
from .ocr.receipt_parser import extract_receipt_data
from .models import Transaction
import os
from .models import User, Expense, Income, Goal,GoalContribution
from .forms import SignUpForm
from .forms import GoalForm
from .forms import GoalContributionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import GoalContribution, Goal
<<<<<<< HEAD
from myapp.services.ai_insights import generate_ai_insights
from .models import Transaction
from datetime import timedelta
from .services.financial_analysis import (
    get_user_financial_snapshot,
    get_missed_deadline_goal
)
from .services.recommendation_engine import generate_smart_recommendations

from django.http import JsonResponse
from datetime import date, timedelta, datetime
import calendar
from django.db import models
import numpy as np

# ---------------- Static Pages ----------------
def budget(request):return render(request, 'myapp/budget.html')
def review(request): return render(request, 'myapp/review.html')
def help_view(request): return render(request, 'myapp/help.html')
def profile(request): return render(request, 'myapp/profile.html')
def settings_view(request): return render(request, 'myapp/settings.html')
def chatbot(request): return render(request, 'myapp/chatbot.html')
=======

import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import PasswordResetOTP
from django.contrib.auth import get_user_model
User = get_user_model()


>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310


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
<<<<<<< HEAD

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



=======
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
# ---------------- Home / Dashboard ----------------
@login_required(login_url='signin')
def home(request):
    user = request.user

    # 1. HANDLE ADD TRANSACTION
    if request.method == "POST":
        try:
            amount = request.POST.get("amount")
            transaction_type = request.POST.get("transaction_type")
            category = request.POST.get("category")
            date_val = request.POST.get("date") or timezone.now().date()

            if not amount:
                messages.error(request, "Amount is required.")
                return redirect('home')

            amount = Decimal(amount)

            if transaction_type == "expense":
                Expense.objects.create(
                    user=user, amount=amount, category=category,
                    description=category, date=date_val
                )
                messages.success(request, f"Expense of Rs. {amount} added successfully!")
            elif transaction_type == "income":
                Income.objects.create(
                    user=user, amount=amount, category=category,
                    description=category, date=date_val
                )
                messages.success(request, f"Income of Rs. {amount} added successfully!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('home')

    # 2. DASHBOARD TOTALS
    # We fetch fresh querysets here to ensure clean data
    all_expenses = Expense.objects.filter(user=user)
    all_incomes = Income.objects.filter(user=user)

    total_income = all_incomes.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expense = all_expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    balance = total_income - total_expense

    # 3. GROUPED DATA FOR PIE CHART (FIXES MULTIPLE FOOD ENTRIES)
    # .order_by() is empty to stop date-sorting from breaking the group
    category_data = all_expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # 4. QUICK STATS
    total_count = all_expenses.count() + all_incomes.count()
    avg_transaction = all_expenses.aggregate(Avg('amount'))['amount__avg'] or 0
    largest_expense = all_expenses.aggregate(Max('amount'))['amount__max'] or 0
    net_change = total_income - total_expense

    # 5. RECENT TRANSACTIONS (FOR THE TABLE)
    recent_incomes = list(all_incomes.order_by('-date')[:10])
    recent_expenses = list(all_expenses.order_by('-date')[:10])

    for i in recent_incomes: i.transaction_type = 'Income'
    for e in recent_expenses: e.transaction_type = 'Expense'

    transactions = sorted(
        recent_incomes + recent_expenses,
        key=lambda x: x.date,
        reverse=True
    )[:10]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'transactions': transactions,
        'category_data': category_data,
        'total_count': total_count,
        'avg_transaction': avg_transaction,
        'largest_expense': largest_expense,
        'net_change': net_change,
    }

    return render(request, 'myapp/home.html', context)
# ---------------- Goals ----------------
<<<<<<< HEAD
@login_required(login_url='signin')
def goals(request):
    user = request.user

    # ---------------- Handle Goal Form ----------------
=======

@login_required(login_url='signin')
def goals(request):

    
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
<<<<<<< HEAD
            goal.user = user
=======
            goal.user = request.user
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
            goal.save()
            messages.success(request, "Goal added successfully!")
            return redirect('goals')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GoalForm()

<<<<<<< HEAD
    # ---------------- Fetch Goals ----------------
    user_goals = Goal.objects.filter(user=user)

    # ---------------- Overview Calculations ----------------
    total_goals = user_goals.count()
    completed_goals = sum(1 for g in user_goals if g.contributions.aggregate(Sum('amount'))['amount__sum'] or 0 >= g.target_amount)
    total_target = sum(g.target_amount for g in user_goals) if user_goals else Decimal('0.00')
    total_saved = sum(g.contributions.aggregate(Sum('amount'))['amount__sum'] or 0 for g in user_goals) if user_goals else Decimal('0.00')
    overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0

    # ---------------- Milestones ----------------
=======
    user_goals = Goal.objects.filter(user=request.user)
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
    icon_map = {
        "First Quarter": "fas fa-seedling",
        "Halfway There": "fas fa-flag",
        "Final Stretch": "fas fa-flag-checkered",
        "Goal Achieved": "fas fa-star"
    }

    for goal in user_goals:
<<<<<<< HEAD
        total = goal.contributions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        goal.total_contributed = total
        goal.remaining_amount = goal.target_amount - total
        goal.progress_percent = min(
            (total / goal.target_amount * 100) if goal.target_amount > 0 else 0,
            100
        )

        if goal.target_date:
            remaining_days = (goal.target_date - date.today()).days
            goal.days_remaining = max(remaining_days, 0)
        else:
            goal.days_remaining = None

        # Dynamic Milestones
        milestone_amounts = [0.25, 0.5, 0.75, 1.0]
        milestone_names = ["First Quarter", "Halfway There", "Final Stretch", "Goal Achieved"]
        milestones = []
        active_set = False
        for perc, name in zip(milestone_amounts, milestone_names):
            amount_m = goal.target_amount * Decimal(perc)
            if total >= amount_m:
=======
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
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
                status = "completed"
            elif not active_set:
                status = "active"
                active_set = True
            else:
                status = "upcoming"
<<<<<<< HEAD
            milestones.append({
                "name": name,
                "amount": float(amount_m),
                "status": status,
                "icon": icon_map[name]
            })
        goal.dynamic_milestones = milestones

    # ---------------- Smart Recommendations ----------------
    financials = get_user_financial_snapshot(user)
    smart_recs = generate_smart_recommendations(user, user_goals, financials)
    missed_goal = get_missed_deadline_goal(user_goals)
    auto_saving = round(financials["expense"] * 0.10, 2)

    # ---------------- Render Context ----------------
    context = {
        "user_goals": user_goals,
        "form": form,
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "total_target": total_target,
        "total_saved": total_saved,
        "overall_progress": min(round(overall_progress, 2), 100),

        # AI Recommendations
        "smart_recommendations": smart_recs,
        "missed_deadline_goal": missed_goal,
        "saving_capacity": round(financials["saving_capacity"], 2),
        "auto_saving": auto_saving,
    }

    return render(request, "myapp/goals.html", context)
=======
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

>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310


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
<<<<<<< HEAD
@login_required(login_url='signin')
def review(request):
    user = request.user

    expenses = Expense.objects.filter(user=user)
    incomes = Income.objects.filter(user=user)

    # Totals
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    filtered_total = total_income - total_expense

    income_count = incomes.count()
    expense_count = expenses.count()
    total_count = income_count + expense_count

    # Combine transactions
    expense_list = list(expenses)
    income_list = list(incomes)

    for e in expense_list:
        e.transaction_type = "Expense"

    for i in income_list:
        i.transaction_type = "Income"

    transactions = sorted(
        expense_list + income_list,
        key=lambda x: x.date,
        reverse=True
    )

    # 🔥 USE AI SERVICE (THIS WAS MISSING)
    ai_insights = generate_ai_insights(transactions)

    context = {
        "transactions": transactions,

        "filtered_total": filtered_total,
        "total_income": total_income,
        "total_expense": total_expense,

        "income_count": income_count,
        "expense_count": expense_count,
        "total_count": total_count,

        # AI DATA
        "ai": ai_insights
    }

    return render(request, "myapp/review.html", context)



@login_required(login_url='sigin')
def analytics(request):
    user=request.user
    today=date.today()
    
    #display info
    month_income=Income.objects.filter(user=user, date__year=today.year, date__month=today.month).aggregate(Sum('amount'))['amount__sum'] or 0
    month_expense=Expense.objects.filter(user=user,date__year=today.year, date__month=today.month).aggregate(Sum('amount'))['amount__sum'] or 0

    active_months=Expense.objects.filter(user=user).dates('date','month').count() or 1
    total_income=Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense=Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    avg_income=total_income / active_months
    avg_expense=total_expense / active_months

    #for monthly history
    monthly_history=[]
    recent_months=Expense.objects.filter(user=user).annotate(
        m=ExtractMonth('date'),
        y=ExtractYear('date')
    ).values('m','y').distinct().order_by('-y','-m')[:6]

    for item in recent_months:
        m_inc=Income.objects.filter(user=user,date__year=item['y'], date__month=item['m']).aggregate(Sum('amount'))['amount__sum'] or 0
        m_exp=Expense.objects.filter(user=user,date__year=item['y'], date__month=item['m']).aggregate(Sum('amount'))['amount__sum'] or 0
        m_count=Expense.objects.filter(user=user,date__year=item['y'], date__month=item['m']).count() + \
                Income.objects.filter(user=user,date__year=item['y'], date__month=item['m']).count()
        
        monthly_history.append({
            'name': calendar.month_name[item['m']],
            'year': item['y'],
            'income': m_inc,
            'expense': m_exp,
            'count': m_count
        })
    
    category_summary=(
        Expense.objects.filter(user=user, date__year=today.year, date__month=today.month)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    top_categories=[]
    for cat in category_summary:
        percentage=(cat['total']/month_expense * 100) if month_expense > 0 else 0
        top_categories.append({
            'category': cat['category'],
            'total': float(cat['total']),
            'percentage': round(percentage,1)
        })

    context = {
        'month_income': month_income,
        'month_expense': month_expense,
        'avg_income': avg_income,
        'avg_expense': avg_expense,
        'monthly_history': monthly_history,
        'top_categories': top_categories,
        }
    return render(request, 'myapp/analytics.html', context)


#Analytics graphs
@login_required(login_url='signin')
def weekly_summary_api(request):
    try:
        start_str=request.GET.get('start')
        end_str=request.GET.get('end')

        if start_str and end_str:
            try:
                start=datetime.strptime(start_str,"%Y-%m-%d").date()
                end=datetime.strptime(end_str,"%Y-%m-%d").date()

            except ValueError:
                end=date.today()
                start=end-timedelta(days=7)

        else:
            end=date.today()
            start=end-timedelta(days=7)

        income = (
            Income.objects
            .filter(user=request.user, date__range=[start, end])
            .values('date')
            .annotate(total=Sum('amount'), type=models.Value('income'))
        )

        expense = (
            Expense.objects
            .filter(user=request.user, date__range=[start, end])
            .values('date')
            .annotate(total=Sum('amount'), type=models.Value('expense'))
        )

        data = list(income) + list(expense)
        return JsonResponse({
                        "start":start,
                        "end":end,
                        "data":list(data)  })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#Pie Chart
@login_required(login_url='signin')
def monthly_category_api(request):
    try:
        today=date.today()
        year=int(request.GET.get('year',today.year))
        month=int(request.GET.get('month',today.month))


        data=(
            Expense.objects
            .filter(user=request.user,date__year=year,date__month=month)
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        return JsonResponse({
            "year":year,
            "month":month,
            "data":list(data) })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#Line Graph
def category_trend_api(request):
    try:
        today=date.today()
        year=int(request.GET.get('year',today.year))
        month=int(request.GET.get('month',today.month))
        category=request.GET.get('category')
        days_in_month = calendar.monthrange(year,month)[1]
    
        if not category:
            return JsonResponse({'error': 'Category missing'}, status=400)


        qs=(
            Expense.objects
            .filter(user=request.user,category=category,date__year=year,date__month=month)
            .values('date')
            .annotate(total=Sum('amount'))
            .order_by('date')
        )

        days=[
            date(year,month,d).isoformat()
            for d in range(1, days_in_month+1)
        ]

        values=[0]*days_in_month

        for entry in qs:
            index=days.index(entry['date'].isoformat())
            values[index]=entry['total']

        days_nums=np.arange(1,days_in_month+1)
        values_array=np.array(values)

        #min two values needed
        if len(values_array[values_array>0])>=2:
            m,b=np.polyfit(days_nums.astype(float),values_array.astype(float), 1)
            predicted_values=[max(0,float(m*x+b)) for x in days_nums]
        
        else:
            predicted_values=values

        return JsonResponse({
            "year":year,
            "month":month,
            "category":category,
            "days":days,
            "values":values,
            "predicted":predicted_values
            })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


              

# ---------------- Static Pages ----------------
def budget(request):return render(request, 'myapp/budget.html')
=======


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import PasswordResetOTP
import random
from django.utils import timezone

User = get_user_model()

# ---------------- Helper function ----------------
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    # Replace with your email backend logic
    print(f"Sending OTP {otp} to {email}")  # DEBUG only
    # send_mail('Your OTP', f'Your OTP is {otp}', 'from@example.com', [email])

# ---------------- Forgot Password ----------------
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            otp = generate_otp()
            PasswordResetOTP.objects.create(user=user, otp=otp, created_at=timezone.now())
            send_otp_email(email, otp)
            request.session['reset_user'] = user.id
            messages.success(request, "OTP sent to your email")
            return redirect("verify_otp")
        else:
            messages.error(request, "No account found with this email")
    return render(request, "myapp/forgot_password.html")
from django.core.mail import send_mail

def send_otp_email(email, otp):
    subject = "Your OTP for Password Reset"
    message = f"Hello!\n\nYour OTP is: {otp}\nIt is valid for 5 minutes."
    from_email = None  # uses DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


# ---------------- Verify OTP ----------------
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        user_id = request.session.get('reset_user')
        otp_obj = PasswordResetOTP.objects.filter(user_id=user_id, otp=otp).last()

        if otp_obj and (timezone.now() - otp_obj.created_at).total_seconds() < 300:  # 5 min expiry
            messages.success(request, "OTP verified! Please reset your password")
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid or expired OTP")

    return render(request, "myapp/verify_otp.html")


# ---------------- Reset Password ----------------
def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user_id = request.session.get('reset_user')
            user = User.objects.get(id=user_id)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully! You can now sign in.")
            return redirect("signin")
    return render(request, "myapp/reset_password.html")
from datetime import datetime
from django.db.models import Sum
from .models import Budget, MoneyFlow, Expense

@login_required
def budget_view(request):
    now = datetime.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))

    # --- NEW: ADD SAVING LOGIC HERE ---
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'add_category':
            category_name = request.POST.get('category')
            amount = request.POST.get('amount')
            icon = request.POST.get('icon', '💰')

            # Create the budget record
            Budget.objects.create(
                user=request.user,
                category=category_name,
                amount=amount,
                icon=icon,
                month=month,
                year=year
            )
        
        elif form_type == 'add_party':
            person_name = request.POST.get('person_name')
            amount = request.POST.get('amount')
            flow_type = request.POST.get('flow_type')

            MoneyFlow.objects.create(
                user=request.user,
                person_name=person_name,
                amount=amount,
                flow_type=flow_type
            )
        
        return redirect('budget') # Refresh page to show new data

    # --- EXISTING DISPLAY LOGIC ---
    budgets = Budget.objects.filter(user=request.user, month=month, year=year)
    budget_data = []
    total_budget = 0
    total_spent = 0

    for b in budgets:
        spent = Expense.objects.filter(
            user=request.user,
            category=b.category,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        remaining = b.amount - spent
        percent = (spent / b.amount * 100) if b.amount > 0 else 0
        
        budget_data.append({
            'obj': b,
            'spent': spent,
            'remaining': remaining,
            'percent': round(percent, 1),
            'is_over': spent > b.amount
        })
        
        total_budget += b.amount
        total_spent += spent

    flows = MoneyFlow.objects.filter(user=request.user)
    you_owe_list = flows.filter(flow_type='topay')
    owed_to_you_list = flows.filter(flow_type='toreceive')
    
    you_owe_total = you_owe_list.aggregate(Sum('amount'))['amount__sum'] or 0
    owed_to_you_total = owed_to_you_list.aggregate(Sum('amount'))['amount__sum'] or 0
    net_flow = owed_to_you_total - you_owe_total

    context = {
        'budget_data': budget_data,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining_total': total_budget - total_spent,
        'total_percent': round((total_spent / total_budget * 100), 1) if total_budget > 0 else 0,
        'you_owe_list': you_owe_list,
        'owed_to_you_list': owed_to_you_list,
        'you_owe_total': you_owe_total,
        'owed_to_you_total': owed_to_you_total,
        'net_flow': net_flow,
    }

    return render(request, 'myapp/budget.html', context)
# ---------------- Static Pages ----------------
def analytics(request): return render(request, 'myapp/analytics.html')
def review(request): return render(request, 'myapp/review.html')
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310
def help_view(request): return render(request, 'myapp/help.html')
def profile(request): return render(request, 'myapp/profile.html')
def settings_view(request): return render(request, 'myapp/settings.html')
def chatbot(request): return render(request, 'myapp/chatbot.html')

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
            reply = get_bot_response(message)
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"reply": "Error: " + str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)
@csrf_exempt
@login_required
def scan_receipt(request):
    if request.method == "POST":
        try:
            receipt = request.FILES.get("receipt")
            if not receipt:
                return JsonResponse({"error": "No file uploaded"}, status=400)

            # Save file temporarily
            media_path = os.path.join(os.getcwd(), "media", "receipts")
            os.makedirs(media_path, exist_ok=True)
            save_path = os.path.join(media_path, receipt.name)

            with open(save_path, "wb+") as f:
                for chunk in receipt.chunks():
                    f.write(chunk)

            # 1. OCR Extraction
            data = extract_receipt_data(save_path)

            # 2. Convert string type to Title Case (Income/Expense)
            t_type = str(data["type"]).strip().title()

            # 3. SAVE TO DATABASE (This makes it dynamic!)
            if t_type == "Income":
                Income.objects.create(
                    user=request.user,
                    amount=Decimal(data["amount"]),
                    category=data["category"],
                    description="Scanned Receipt",
                    date=data["date"]
                )
            else:
                Expense.objects.create(
                    user=request.user,
                    amount=Decimal(data["amount"]),
                    category=data["category"],
                    description="Scanned Receipt",
                    date=data["date"]
                )

            return JsonResponse({"status": "success", "amount": data["amount"]})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
<<<<<<< HEAD
    return JsonResponse({"error": "Invalid request"}, status=400)

# transaction deletion

@login_required
@require_POST
def delete_transaction(request):
    data = json.loads(request.body)
    t_id = data.get("id")
    t_type = data.get("type")

    try:
        if t_type == "Expense":
            Expense.objects.get(id=t_id, user=request.user).delete()
        else:
            Income.objects.get(id=t_id, user=request.user).delete()

        # Recalculate totals
        expenses = Expense.objects.filter(user=request.user)
        incomes = Income.objects.filter(user=request.user)

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

        return JsonResponse({
        "success": True,
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "filtered_total": float(total_income - total_expense),
        "total_count": expenses.count() + incomes.count()
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    




#filter and search
from django.db.models import Q

@login_required
def filter_transactions(request):
    search = request.GET.get("search", "").strip()
    type_filter = request.GET.get("type", "All Types")
    category_filter = request.GET.get("category", "All Categories")
    sort_by = request.GET.get("sort", "date_desc")

    # Combine Income and Expense into a single list
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    for e in expenses: e.transaction_type = "Expense"
    for i in incomes: i.transaction_type = "Income"

    transactions = list(expenses) + list(incomes)

    # Apply search and filters
    if search:
        transactions = [t for t in transactions if search.lower() in (t.description or t.category).lower()]

    if type_filter != "All Types":
        transactions = [t for t in transactions if t.transaction_type == type_filter]

    if category_filter != "All Categories":
        transactions = [t for t in transactions if t.category == category_filter]

    # Sorting
    reverse = True
    key_func = lambda t: t.date
    if sort_by == "date_asc": reverse = False
    elif sort_by == "amount_asc": key_func = lambda t: t.amount; reverse = False
    elif sort_by == "amount_desc": key_func = lambda t: t.amount
    elif sort_by == "type_asc": key_func = lambda t: t.transaction_type; reverse = False
    elif sort_by == "type_desc": key_func = lambda t: t.transaction_type

    transactions.sort(key=key_func, reverse=reverse)

    # Prepare summary totals
    total_income = sum(t.amount for t in transactions if t.transaction_type=="Income")
    total_expense = sum(t.amount for t in transactions if t.transaction_type=="Expense")
    filtered_total = total_income - total_expense
    income_count = sum(1 for t in transactions if t.transaction_type=="Income")
    expense_count = sum(1 for t in transactions if t.transaction_type=="Expense")
    total_count = len(transactions)

    transaction_list = []
    for t in transactions:
        transaction_list.append({
            "id": t.id,
            "description": t.description or t.category,
            "category": t.category,
            "transaction_type": t.transaction_type,
            "amount": float(t.amount),
            "date": t.date.strftime("%Y-%m-%d")
        })

    return JsonResponse({
        "transactions": transaction_list,
        "filtered_total": filtered_total,
        "total_income": total_income,
        "total_expense": total_expense,
        "income_count": income_count,
        "expense_count": expense_count,
        "total_count": total_count
    })

#delete transactions home page
@login_required
@require_POST
def delete_transactionhome(request):
    import json
    from django.db.models import Sum, Max, Avg
    data = json.loads(request.body)
    t_id = data.get("id")
    t_type = data.get("type")

    try:
        if t_type == "Expense":
            trans = Expense.objects.get(id=t_id, user=request.user)
        else:
            trans = Income.objects.get(id=t_id, user=request.user)
        trans.delete()

        # Recalculate transactions
        expenses = Expense.objects.filter(user=request.user)
        incomes = Income.objects.filter(user=request.user)

        total_income = sum(i.amount for i in incomes)
        total_expense = sum(e.amount for e in expenses)
        balance = total_income - total_expense
        total_count = expenses.count() + incomes.count()
        avg_transaction = (sum([t.amount for t in list(expenses) + list(incomes)]) / total_count) if total_count > 0 else 0
        largest_expense = max([e.amount for e in expenses], default=0)
        avg_expense = (sum(e.amount for e in expenses) / expenses.count()) if expenses.exists() else 0


        # Category data for chart
        categories = {}
        for e in expenses:
            categories[e.category] = categories.get(e.category, 0) + float(e.amount)

        category_data = [{"category": k, "total": v} for k, v in categories.items()]

        # Progress bar percentage (expenses / income)
        progress_percentage = (total_expense / total_income * 100) if total_income > 0 else 0

        return JsonResponse({
            "success": True,
            "balance": float(balance),
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "total_count": total_count,
            "avg_transaction": float(avg_transaction),
            "largest_expense": float(largest_expense),
            "category_data": category_data,
            "progress_percentage": float(progress_percentage)
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
=======
    return JsonResponse({"error": "Invalid request"}, status=400)
>>>>>>> 1b48a6279169d56bfffdc2a42aa5f29db03b0310

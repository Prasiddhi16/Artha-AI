from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
import random, time
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from .models import User, Expense, Income, Goal
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import Max
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
from myapp.services.ai_insights import generate_ai_insights
from .models import Transaction
from datetime import timedelta
from datetime import date
from .models import NotificationEvent
from .utils import create_notification
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
from .forms import BudgetForm, MoneyFlowForm
from .models import Budget, MoneyFlow, Expense
from .forms import ProfileForm, NotificationForm, PrivacySettingsForm, PasswordUpdateForm
from .models import Notification, PrivacySettings
from django.contrib.auth import update_session_auth_hash

<<<<<<< HEAD
=======

>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e
# ---------------- Static Pages ----------------

def review(request): return render(request, 'myapp/review.html')
def help_view(request): return render(request, 'myapp/help.html')
def profile(request): return render(request, 'myapp/profile.html')
def settings_view(request): return render(request, 'myapp/settings.html')
def chatbot(request): return render(request, 'myapp/chatbot.html')


# ---------------- Signup ----------------
<<<<<<< HEAD

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


=======
>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e
import random
from django.shortcuts import render, redirect

from django.core.mail import send_mail
from .models import EmailOTP
from django.contrib.auth import get_user_model
User = get_user_model()

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # basic validation
        if not name or not email or not password:
            messages.error(request, "All fields are required")
            return redirect("signup")
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect("signup")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

<<<<<<< HEAD
        # ✅ CORRECT user creation
=======
        #user creation
>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password
        )

        user.is_active = False  # block login until verified
<<<<<<< HEAD
=======
        user.is_email_verified = False
>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e
        user.save()

        # OTP
        otp = str(random.randint(100000, 999999))
<<<<<<< HEAD
        EmailOTP.objects.create(user=user, otp=otp)
=======
        EmailOTP.objects.create(user=user, otp=otp, purpose="signup")

        # SAVE USER ID IN SESSION
        request.session['otp_user_id'] = user.id
        request.session['otp_purpose'] = "signup"
>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e

        send_mail(
    "Email Verification – Artha AI",
    f"""Hello,

Thank you for registering with Artha AI.

To verify your email address, please use the One-Time Password (OTP) below:

OTP: {otp}

This OTP is valid for 5 minutes only. Please do not share this code with anyone.

If you did not request this verification, please ignore this email.

Thank you for choosing Artha AI.

Kind regards,
Artha AI Team
""",
    None,   # uses DEFAULT_FROM_EMAIL
    [email],
    fail_silently=False,
)


        return redirect("verify_email")

    return render(request, "myapp/signup.html")


<<<<<<< HEAD
def verify_email(request):
    if request.method == "POST":
        otp = request.POST.get("otp")

        otp_obj = EmailOTP.objects.filter(otp=otp).first()

        if otp_obj and not otp_obj.is_expired():
            user = otp_obj.user
            user.is_active = True
            user.is_email_verified = True
            user.save()
            otp_obj.delete()
            messages.success(request, "Email verified successfully!")
            return redirect("signin")
        else:
            messages.error(request, "Invalid or expired OTP")

    return render(request, "myapp/verify_email.html")

=======
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

def verify_email(request):
    if request.method == "POST":

        if request.content_type == "application/json":
            data = json.loads(request.body)
            otp_input = data.get("otp")
            is_ajax = True
        else:
            otp_input = request.POST.get("otp")
            is_ajax = False

        user_id = request.session.get("otp_user_id")
        purpose = request.session.get("otp_purpose")

        if not user_id or not purpose:
            msg = "Session expired. Please try again."
            if is_ajax:
                return JsonResponse({"success": False, "message": msg})
            messages.error(request, msg)
            return redirect("signup")

        otp_obj = EmailOTP.objects.filter(
            user_id=user_id,
            otp=otp_input,
            purpose=purpose
        ).first()

        if not otp_obj:
            msg = "Invalid OTP"
            if is_ajax:
                return JsonResponse({"success": False, "message": msg})
            messages.error(request, msg)
            return redirect("verify_email")

        if otp_obj.is_expired():
            otp_obj.delete()
            msg = "OTP expired"
            if is_ajax:
                return JsonResponse({"success": False, "message": msg})
            messages.error(request, msg)
            return redirect("verify_email")

        
        user = otp_obj.user

        if purpose == "signup":
            user.is_active = True
            user.is_email_verified = True

        elif purpose == "change_email":
            user.email = request.session.get("new_email")
            user.is_email_verified = True

        user.save()
        otp_obj.delete()
        request.session.flush()

        msg = "Email verified successfully!"

        if is_ajax:
            return JsonResponse({
                "success": True,
                "message": msg,
                "new_email": user.email
            })

        messages.success(request, msg)
        return redirect("signin")

    return render(request, "myapp/verify_email.html")


>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def set_password(request):
    user = request.user

    # If password already exists, block access
    if user.has_usable_password():
        return redirect('signin')

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return render(request, "set_password.html")

        user.set_password(password)
        user.save()

        messages.success(request, "Account created. Please sign in.")
        return redirect("signin")

    return render(request, "myapp/set_password.html")



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


# ---------------- Home / Dashboard ----------------
from myapp.utils import create_notification
from django.contrib.auth import get_user_model

@login_required(login_url='signin')
def home(request):
    user = request.user

    # Initialize variables
    amount = None
    transaction_type = None
    category = None
    date_val = timezone.now().date()

    # ---------------- POST: Add Transaction ----------------
    if request.method == "POST":
        amount = request.POST.get("amount")
        transaction_type = request.POST.get("transaction_type", "").capitalize()
        category = request.POST.get("category")
        date_str = request.POST.get("date")

        date_val = timezone.now().date()
        if date_str:
            try:
                date_val = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount")
            return redirect('home')

        # Save Transaction first
        if transaction_type == "Expense":
            trans = Expense.objects.create(
                user=user,
                amount=amount,
                category=category,
                date=date_val
            )
        elif transaction_type == "Income":
            trans = Income.objects.create(
                user=user,
                amount=amount,
                category=category,
                date=date_val
            )
            # After saving the transaction
            create_notification(user, "DEBUG: Transaction POST reached", "info")


        # ---------------- Notifications ----------------
        # High Spending
        high_limit = getattr(user, 'high_spending_limit', 5000)
        if transaction_type == "Expense" and amount >= high_limit:
            create_notification(
                user=user,
                message=f"⚠️ High Spending Alert: You spent ₹{amount} on {category}",
                notification_type="warning"
            )

        # Category Budget
        if transaction_type == "Expense":
            category_budget = (
                Budget.objects.filter(
                    user=user,
                    category=category,
                    month=date_val.month,
                    year=date_val.year
                ).aggregate(Sum('amount'))['amount__sum'] or 0
            )
            category_total = Expense.objects.filter(
                user=user,
                category=category,
                date__month=date_val.month,
                date__year=date_val.year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            if category_budget > 0 and category_total >= category_budget:
                create_notification(
                    user=user,
                    message=f"📊 Budget Alert: {category} budget exceeded (₹{category_budget})",
                    notification_type="warning"
                )

        # Large Income
        if transaction_type == "Income" and amount >= 20000:
            create_notification(
                user=user,
                message=f"💰 Large Income Alert: ₹{amount} received",
                notification_type="success"
            )

        # Low Balance
        total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        total_expense = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        balance = total_income - total_expense
        low_balance_limit = getattr(user, 'low_balance_limit', 1000)

        if balance <= low_balance_limit:
            if not NotificationEvent.objects.filter(
                user=user,
                message__icontains="Low Balance",
                created_at__date=timezone.now().date()
            ).exists():
                create_notification(
                    user=user,
                    message=f"⚠️ Low Balance Alert: Your current balance is ₹{balance}",
                    notification_type="warning"
                )

        # Done
        return redirect('home')



    # ---------------- DASHBOARD DATA ----------------
    all_expenses = Expense.objects.filter(user=user)
    all_incomes = Income.objects.filter(user=user)

    total_income = all_incomes.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expense = all_expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    balance = total_income - total_expense

    # Low Balance Alert
    low_balance_limit = getattr(user, 'low_balance_limit', 1000)
    if balance <= low_balance_limit:
        if not NotificationEvent.objects.filter(
            user=user,
            message__icontains="Low Balance",
            created_at__date=timezone.now().date()
        ).exists():
            create_notification(
                user,
                f"⚠️ Low Balance Alert: Your current balance is ₹{balance}",
                "warning"
            )

    # Category Pie Chart
    category_data = all_expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Quick Stats
    total_count = all_expenses.count() + all_incomes.count()
    avg_transaction = all_expenses.aggregate(Avg('amount'))['amount__avg'] or 0
    largest_expense = all_expenses.aggregate(Max('amount'))['amount__max'] or 0
    net_change = total_income - total_expense

    # Recent Transactions
    recent_incomes = list(all_incomes.order_by('-date')[:10])
    recent_expenses = list(all_expenses.order_by('-date')[:10])

    for i in recent_incomes: i.transaction_type = 'Income'
    for e in recent_expenses: e.transaction_type = 'Expense'

    transactions = sorted(
        recent_incomes + recent_expenses,
        key=lambda x: x.date,
        reverse=True
    )[:10]

   # Optional: Auto-Saving Notification
    financials = get_user_financial_snapshot(user)
    auto_saving = round(financials.get("expense", 0) * 0.10, 2)

    if auto_saving >= 1000:
        msg = f"💡 Smart Tip: You could save ₹{auto_saving} this month"

        # Only create the notification if it doesn't already exist
        if not NotificationEvent.objects.filter(user=user, message=msg, is_read=False).exists():
            NotificationEvent.objects.create(
                user=user,
                message=msg,
                notification_type="info"
            )

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
@login_required(login_url='signin')
def goals(request):
    user = request.user

    # ---------------- Handle Goal Form ----------------
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = user
            goal.save()
            messages.success(request, "Goal added successfully!")
            return redirect('goals')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GoalForm()

    # ---------------- Fetch Goals ----------------
    user_goals = Goal.objects.filter(user=user)

    # ---------------- Overview Calculations ----------------
    total_goals = user_goals.count()
    completed_goals = sum(1 for g in user_goals if g.contributions.aggregate(Sum('amount'))['amount__sum'] or 0 >= g.target_amount)
    total_target = sum(g.target_amount for g in user_goals) if user_goals else Decimal('0.00')
    total_saved = sum(g.contributions.aggregate(Sum('amount'))['amount__sum'] or 0 for g in user_goals) if user_goals else Decimal('0.00')
    overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0

    # ---------------- Milestones ----------------
    icon_map = {
        "First Quarter": "fas fa-seedling",
        "Halfway There": "fas fa-flag",
        "Final Stretch": "fas fa-flag-checkered",
        "Goal Achieved": "fas fa-star"
    }

    for goal in user_goals:
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
                status = "completed"
            elif not active_set:
                status = "active"
                active_set = True
            else:
                status = "upcoming"
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
            contribution.save()

        new_total = goal.contributions.aggregate(
            Sum('amount')
        )['amount__sum'] or Decimal('0.00')

        if new_total >= goal.target_amount:
            create_notification(
                user=request.user,
                message=f"🎉 You have completed the goal '{goal.title}'!",
                notification_type="success"
            )

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

        contribution = GoalContribution.objects.create(
    user=request.user,
    goal=goal,
    amount=amount,
    date=date,
    note=note
)

# Recalculate after saving
        total = goal.contributions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

        if total >= goal.target_amount:
            create_notification(
                user=request.user,
                message=f"🎉 You have completed the goal '{goal.title}'!",
                notification_type="success"
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
    if not contributions.exists():
        return JsonResponse({
            "empty": True,
            "goal_title": goal.title
        })

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

    #  USE AI SERVICE (THIS WAS MISSING)
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



@login_required(login_url='signin')
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
    
    # Get months with expenses
    expense_months = Expense.objects.filter(user=user).annotate(
        m=ExtractMonth('date'),
        y=ExtractYear('date')
    ).values('m','y').distinct()
    
    # Get months with income
    income_months = Income.objects.filter(user=user).annotate(
        m=ExtractMonth('date'),
        y=ExtractYear('date')
    ).values('m','y').distinct()
    
    # Combine and deduplicate months
    all_months = {}
    for item in expense_months:
        key = (item['y'], item['m'])
        all_months[key] = {'y': item['y'], 'm': item['m']}
    
    for item in income_months:
        key = (item['y'], item['m'])
        if key not in all_months:
            all_months[key] = {'y': item['y'], 'm': item['m']}
    
    # Sort by year and month, get recent 6
    recent_months = sorted(all_months.values(), key=lambda x: (x['y'], x['m']), reverse=True)[:6]

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

        actual_values=[0.0]*days_in_month

        for entry in qs:
            index=days.index(entry['date'].isoformat())
            actual_values[index] = float(entry['total'])

        is_current_month = (year == today.year and month == today.month)
        current_day_index = min(today.day - 1, days_in_month - 1) if is_current_month else days_in_month - 1

        days_nums=np.arange(1,days_in_month+1)
        
        #Create predicted values array
        predicted_values = [None] * days_in_month

        # Only predict if we have at least 2 non-zero values up to current day
        values_for_prediction = actual_values[:current_day_index + 1] if is_current_month else actual_values
        days_for_prediction = days_nums[:current_day_index + 1] if is_current_month else days_nums
        
        non_zero_indices = [i for i, v in enumerate(values_for_prediction) if float(v) > 0]
        non_zero_count = len(non_zero_indices)
       
        prediction_info = {}
        
        if non_zero_count >= 2:
            weights = np.ones(len(values_for_prediction))
            for i in non_zero_indices:
                # Recent days get higher weights (exponential weighting)
                weights[i] = np.exp((i - len(values_for_prediction)) / 10) + 1
            
            # Weighted polynomial fit (degree 1 = linear)
            try:
                days_array = days_for_prediction.astype(float)
                values_array = np.array(values_for_prediction, dtype=float)
                
                m, b = np.polyfit(days_array, values_array, 1, w=weights)
                
              
                predicted_all = m * days_for_prediction + b
                residuals = values_array - predicted_all
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((values_array - np.mean(values_array))**2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
                
                
                if is_current_month:
                    #start from tomorrow
                    for i in range(current_day_index + 1, days_in_month):
                        predicted_values[i] = max(0, float(m * (i + 1) + b))
                else:
                    
                    for i in range(days_in_month):
                        predicted_values[i] = max(0, float(m * (i + 1) + b))
                
                
                prediction_info = {
                    "method": "weighted_linear_regression",
                    "r_squared": round(float(r_squared), 3),
                    "accuracy": "good" if r_squared > 0.7 else "moderate" if r_squared > 0.4 else "low",
                    "data_points": non_zero_count
                }
            except Exception as e:
                prediction_info = {"error": str(e)}
        else:
            prediction_info = {
                "method": "insufficient_data",
                "data_points": non_zero_count,
                "message": "Need at least 2 days of expense data for prediction"
            }

        return JsonResponse({
            "year":year,
            "month":month,
            "category":category,
            "days":days,
            "values":actual_values,
            "predicted":predicted_values,
            "current_day": current_day_index +  1 if is_current_month else None,
            "prediction_info": prediction_info  
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


              

# ---------------- Static Pages ----------------
def help_view(request): return render(request, 'myapp/help.html')
def profile(request): return render(request, 'myapp/profile.html')
def settings_view(request): return render(request, 'myapp/settings.html')
def chatbot(request): return render(request, 'myapp/chatbot.html')
def utilities(request):return render(request,'myapp/utilities.html')

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
    return JsonResponse({"error": "Invalid request"}, status=400)

    # ----------------- RECEIPT NOTIFICATION ----------------
    create_notification(
        request.user,
        f"🧾 Receipt added: {data['category']} ₹{data['amount']}",
        "info"
    )
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
    

#budget
@login_required
def budget_view(request):
    # Clear any existing messages at the start of GET request
    if request.method == "GET":
        storage = messages.get_messages(request)
        storage.used = True

    now = datetime.now()
    month = request.GET.get('month', now.month)
    year = request.GET.get('year', now.year)


    try:
        month = int(month)
    except (TypeError, ValueError):
        month = now.month

    try:
        year = int(year)
    except (TypeError, ValueError):
        year = now.year

    months = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
    
    #  post logic
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        month = int(request.POST.get('month', month))
        year = int(request.POST.get('year', year))


        if form_type == 'add_category':
            category = request.POST.get('category')
            amount = request.POST.get('amount')
            
            # Check if budget already exists for this category
            existing_budget = Budget.objects.filter(
                user=request.user,
                category=category,
                month=month,
                year=year
            ).first()
            
            if existing_budget:
                messages.error(
                    request,
                    f"Budget for '{category}' already exists for {months[month-1]} {year}. Please edit the existing budget instead."
                )
                return redirect(f'/budget/?month={month}&year={year}')
            
            # Check if amount is zero or negative
            try:
                amount_value = float(amount)
                if amount_value <= 0:
                    messages.error(
                        request,
                        "Budget amount must be greater than zero."
                    )
                    return redirect(f'/budget/?month={month}&year={year}')
            except (TypeError, ValueError):
                messages.error(
                    request,
                    "Invalid budget amount."
                )
                return redirect(f'/budget/?month={month}&year={year}')
            
            form = BudgetForm(request.POST)
            if form.is_valid():
                budget = form.save(commit=False)
                budget.user = request.user
                budget.month = None
                budget.year = None
                budget.save()

        elif form_type == 'add_party':
            person_name = request.POST.get('person_name')
            flow_type = request.POST.get('flow_type')
            
            # Check if party already exists
            existing_party = MoneyFlow.objects.filter(
                user=request.user,
                person_name__iexact=person_name,
                flow_type=flow_type
            ).first()
            
            if existing_party:
                messages.error(
                    request,
                    f"'{person_name}' already exists in your money flow. Please delete the existing entry to add new."
                )
                return redirect(f'/budget/?month={month}&year={year}')
            
            flow_form = MoneyFlowForm(request.POST)
            if flow_form.is_valid():
                flow = flow_form.save(commit=False)
                flow.user = request.user
                flow.save()

        # Redirect back with the month and year so the data shows up immediately
        return redirect(f'/budget/?month={month}&year={year}')

    # data display
    total_income = Income.objects.filter(user=request.user, date__month=month, date__year=year).aggregate(Sum('amount'))['amount__sum'] or 0
    recommended_budget_limit = float(total_income) * 0.7
    
    total_spent = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).aggregate(Sum('amount'))['amount__sum'] or 0


    #budgets set
    budgets = Budget.objects.filter(user=request.user)

    #All categories with some expense this month
    all_expense_categories = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).values_list('category', flat=True).distinct()

    # Collect all categories (from budgets + expenses)
    budget_categories = set(budgets.values_list('category', flat=True))
    expense_categories_set = set(all_expense_categories)
    all_categories = budget_categories | expense_categories_set

    budget_map = {b.category: b for b in budgets}
    budget_data = []
    total_budget = 0

    for category in all_categories:
        budget = budget_map.get(category)

        spent = Expense.objects.filter(
            user=request.user,
            category=category,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        if budget:
            amount = budget.amount
            remaining = amount - spent
            percent = (spent / amount * 100) if amount > 0 else     (100 if spent > 0 else 0)

            budget_data.append({
                'id': budget.id,
                'category': category,
                'amount': amount,
                'icon': budget.icon,
                'spent': spent,
                'remaining': remaining,
                'percent': round(percent, 1),
                'is_over': spent > amount,
                'has_budget': True
            })

            total_budget += amount

        else:
            budget_data.append({
                'id': None,
                'category': category,
                'amount': 0,
                'icon': '💰',
                'spent': spent,
                'remaining': -spent,
                'percent': 100,
                'is_over': spent > 0,
                'has_budget': False
            })

    # Sort by spent amount (highest first)
    budget_data.sort(key=lambda x: x['spent'], reverse=True)

    
    #money flow
    flows = MoneyFlow.objects.filter(user=request.user)
    you_owe_list = flows.filter(flow_type='topay')
    owed_to_you_list = flows.filter(flow_type='toreceive')

    you_owe_total = you_owe_list.aggregate(Sum('amount'))['amount__sum'] or 0
    owed_to_you_total = owed_to_you_list.aggregate(Sum('amount'))['amount__sum'] or 0
    net_flow = owed_to_you_total - you_owe_total

    #check if overspending
    is_overspending = total_spent > total_budget and total_budget > 0

    context = {
        'now': now,
        'current_month': month,
        'current_year': year,
        'budget_data': budget_data,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining_total': total_budget - total_spent,
        'total_percent': round((total_spent / total_budget * 100), 1) if total_budget > 0 else (100 if total_spent > 0 else 0),
        'you_owe_list': you_owe_list,
        'owed_to_you_list': owed_to_you_list,
        'you_owe_total': you_owe_total,
        'owed_to_you_total': owed_to_you_total,
        'net_flow': net_flow,
        'total_income': total_income,
        'recommended_limit': recommended_budget_limit,
        'allocation_warning': total_budget > recommended_budget_limit,
        'has_any_budget': total_budget > 0,
        'is_overspending': is_overspending
    }

    return render(request, 'myapp/budget.html', context)

@login_required
@require_POST
def edit_budget(request):
    budget_id = request.POST.get('budget_id')
    new_amount = request.POST.get('amount')
    budget_item = get_object_or_404(Budget, id=budget_id, user=request.user)

    month = request.POST.get('month', datetime.now().month)
    year = request.POST.get('year', datetime.now().year)
    
    if new_amount is not None:
        try:
            new_amount = float(new_amount)
        except (TypeError, ValueError):
            messages.error(
                request,
                "Invalid budget amount."
            )
            return redirect(f'/budget/?month={budget_item.month}&year={budget_item.year}')

        if new_amount <= 0:              
            messages.error(
                request,
                "Budget must be greater than zero."
            )
            return redirect(
                f'/budget/?month{month}&year={year}'
            )

        budget_item.amount = new_amount  
        budget_item.save()
        messages.success(
            request,
            f"Updated {budget_item.category}!"
        )

    return redirect(f'/budget/?month={month}&year={year}')

#delete money flow
@login_required
@require_POST
def delete_money_flow(request):
    """Delete a money flow entry"""
    try:
        data = json.loads(request.body)
        flow_id = data.get('flow_id')
        
        flow = MoneyFlow.objects.get(id=flow_id, user=request.user)
        flow.delete()
        
        # Recalculate totals
        flows = MoneyFlow.objects.filter(user=request.user)
        you_owe_total = flows.filter(flow_type='topay').aggregate(Sum('amount'))['amount__sum'] or 0
        owed_to_you_total = flows.filter(flow_type='toreceive').aggregate(Sum('amount'))['amount__sum'] or 0
        net_flow = owed_to_you_total - you_owe_total
        
        return JsonResponse({
            'success': True,
            'you_owe_total': float(you_owe_total),
            'owed_to_you_total': float(owed_to_you_total),
            'net_flow': float(net_flow)
        })
        
    except MoneyFlow.DoesNotExist:
        return JsonResponse({'error': 'Entry not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
def delete_budget(request):
    budget_id = request.POST.get('budget_id')
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    month = request.POST.get('month', datetime.now().month)
    year = request.POST.get('year', datetime.now().year)

    #Checking if expenses exist for this category
    has_expenses = Expense.objects.filter(
        user=request.user,
        category=budget.category,
        date__month=budget.month,
        date__year=budget.year
    ).exists()

    if has_expenses:
        messages.error(
            request,
            f"Cannot delete '{budget.category}' because expenses exist."
        )
    else:
        budget.delete()
        messages.success(
            request,
            f"Deleted budget '{budget.category}'."
        )

    return redirect(f'/budget/?month={month}&year={year}')

#profile
@login_required
def profile(request):
    user = request.user
    

    notification_settings, _ = Notification.objects.get_or_create(user=user,defaults={
            'email_notifications': False,
            'push_notifications': False,
            'monthly_reports': False,
            'budget_alerts': False,
            'goal_reminders': False
        })
    privacy_settings, _ = PrivacySettings.objects.get_or_create(user=user,
        defaults={
            'analytics_tracking': False,
            'crash_reporting': False,
            'usage_data': False,
            'spending_insights': False,
            'two_factor_auth': False
        })
    
    # Initialize forms
    profile_form = ProfileForm(instance=user)
    notification_form = NotificationForm(instance=notification_settings)
    privacy_form = PrivacySettingsForm(instance=privacy_settings)
    password_form = PasswordUpdateForm(user=user)

    
    context = {
        'user': user,
        'profile_form': profile_form,
        'notification_form': notification_form,
        'privacy_form': privacy_form,
        'password_form': password_form,
        'privacy_settings':privacy_settings,
        'notification_settings':notification_settings

    }
    
    return render(request, 'myapp/profile.html', context)

@login_required
@require_POST
def update_profile(request):
    try:
        data = json.loads(request.body)
        user = request.user

        # Validate fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        
        if not name or len(name) < 2:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid name. Name must be at least 2 characters long.'
            }, status=400)
        
        if not email or '@' not in email:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            }, status=400)
        
        # Check if email is already taken by another user
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return JsonResponse({
                'success': False,
                'message': 'This email is already in use.'
            }, status=400)
        
        user.name = data.get('name')
        user.email = data.get('email')
        user.phone = data.get('phone')
        user.save()
        return JsonResponse({'message': 'Profile updated successfully!'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

@login_required
@require_POST
def update_notifications(request):
    """Handle AJAX notification settings update"""
    try:
        data = json.loads(request.body)
        notification_settings, _ = Notification.objects.get_or_create(user=request.user)
        
        notification_settings.email_notifications = data.get('email_notifications', False)
        notification_settings.push_notifications = data.get('push_notifications', False)
        notification_settings.monthly_reports = data.get('monthly_reports', False)
        notification_settings.budget_alerts = data.get('budget_alerts', False)
        notification_settings.goal_reminders = data.get('goal_reminders', False)

        notification_settings.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification preferences saved successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def update_password(request):
    """Handle AJAX password update"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        # Check current password
        if not user.check_password(data.get('current_password')):
            return JsonResponse({
                'success': False,
                'message': 'Current password is incorrect.'
            }, status=400)
        
        # Check if new passwords match
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if new_password != confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'New passwords do not match.'
            }, status=400)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Keep user logged in after password change
        update_session_auth_hash(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Password updated successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def update_privacy_settings(request):
    """Handle AJAX privacy settings update"""
    try:
        data = json.loads(request.body)
        privacy_settings, _ = PrivacySettings.objects.get_or_create(user=request.user)
        
        privacy_settings.analytics_tracking = data.get('analytics_tracking', False)
        privacy_settings.crash_reporting = data.get('crash_reporting', False)
        privacy_settings.usage_data = data.get('usage_data', False)
        privacy_settings.spending_insights = data.get('spending_insights', False)
        privacy_settings.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Privacy settings saved successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def toggle_two_factor(request):
    """Toggle two-factor authentication"""
    try:
        data = json.loads(request.body)
        privacy_settings, _ = PrivacySettings.objects.get_or_create(user=request.user)
        
        privacy_settings.two_factor_auth = data.get('enabled', False)
        privacy_settings.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Two-factor authentication {"enabled" if privacy_settings.two_factor_auth else "disabled"}.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def request_email_change(request):
    data = json.loads(request.body)
    new_email = data.get("new_email")

    if not new_email:
        return JsonResponse({"success": False, "message": "Email required"})

    if User.objects.filter(email=new_email).exists():
        return JsonResponse({"success": False, "message": "Email already in use"})

    otp = str(random.randint(100000, 999999))

    EmailOTP.objects.create(
        user=request.user,
        otp=otp,
        purpose="change_email"
    )

    request.session['otp_user_id'] = request.user.id
    request.session['otp_purpose'] = "change_email"
    request.session['new_email'] = new_email

    send_mail(
        "Confirm email change – Artha AI",
        f"""Your OTP is: {otp}
    This OTP is valid for 5 minutes only. Please do not share this code with anyone.
    If you did not request this verification, please ignore this email.        
    Kind regards,
    Artha AI Team
    """,
        None,
        [new_email],
        fail_silently=False
    )
    return JsonResponse({"success": True,
                         "message": "OTP sent to new email"})


@login_required
@require_POST
def delete_account(request):
    """Handle account deletion"""
    try:
        user = request.user
        user.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Account deleted successfully.',
            'redirect': '/signin/'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
    
@login_required
def export_settings(request):
    user = request.user
    notification_settings = Notification.objects.get(user=user)
    privacy_settings = PrivacySettings.objects.get(user=user)
    
    settings_data = {
        'user_info': {
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
        },
        'notifications': {
            'email_notifications': notification_settings.email_notifications,
            'push_notifications': notification_settings.push_notifications,
            'monthly_reports': notification_settings.monthly_reports,
            'budget_alerts': notification_settings.budget_alerts,
            'goal_reminders': notification_settings.goal_reminders,
        },
        'privacy': {
            'analytics_tracking': privacy_settings.analytics_tracking,
            'crash_reporting': privacy_settings.crash_reporting,
            'usage_data': privacy_settings.usage_data,
            'spending_insights': privacy_settings.spending_insights,
            'two_factor_auth': privacy_settings.two_factor_auth,
        },
        'exported_at': timezone.now().isoformat()
    }
    response = JsonResponse(settings_data)
    response['Content-Disposition'] = f'attachment; filename="settings_{user.id}.json"'
    return response

@login_required
@require_POST
def clear_all_data(request):
    try:
        data = json.loads(request.body)
        if data.get('confirm') != 'DELETE':
            return JsonResponse({
                'success': False,
                'message': 'Please type DELETE to confirm'
            }, status=400)
        
        user = request.user
        
        # Delete all user data
        Expense.objects.filter(user=user).delete()
        Income.objects.filter(user=user).delete()
        Goal.objects.filter(user=user).delete()
        Budget.objects.filter(user=user).delete()
        MoneyFlow.objects.filter(user=user).delete()
        
        # Reset settings to default
        notification_settings = Notification.objects.get(user=user)
        notification_settings.email_notifications = False
        notification_settings.push_notifications = False
        notification_settings.monthly_reports = False
        notification_settings.budget_alerts = False
        notification_settings.goal_reminders = False
        notification_settings.save()
        
        privacy_settings = PrivacySettings.objects.get(user=user)
        privacy_settings.analytics_tracking = False
        privacy_settings.crash_reporting = False
        privacy_settings.usage_data = False
        privacy_settings.spending_insights = False
        privacy_settings.two_factor_auth = False
        privacy_settings.save()
        
        return JsonResponse({
            'success': True,
            'message': 'All data cleared successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def upload_profile_picture(request):
    image = request.FILES.get("profile_image")

    if not image:
        return JsonResponse({"success": False, "message": "No image uploaded"})

    request.user.profile_image = image
    request.user.save()

    return JsonResponse({
        "success": True,
        "image_url": request.user.profile_image.url
    })
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import NotificationEvent

@login_required
def get_notifications(request):
    # Fetch latest 10 notifications for the logged-in user
    notifications = NotificationEvent.objects.filter(user=request.user).order_by('-created_at')[:10]

    data = [
        {
            "id": n.id,
            "message": n.message,
            "type": n.notification_type,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for n in notifications
    ]
    return JsonResponse({"notifications": data})


@login_required
def mark_notifications_read(request):
    if request.method == "POST":
        NotificationEvent.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "failed"}, status=400)

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import NotificationEvent


@login_required
def clear_notifications(request):
    if request.method == "POST":
        NotificationEvent.objects.filter(
            user=request.user
        ).delete()

        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Invalid method"}, status=405)


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
from .forms import SignUpForm
from .models import GoalContribution
from django.shortcuts import render, redirect, get_object_or_404

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


              
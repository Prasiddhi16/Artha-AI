from django.shortcuts import render

def home(request):
    return render(request, 'myapp/home.html')

def analytics(request):
    return render(request, 'myapp/analytics.html')

def review(request):
    return render(request, 'myapp/review.html')

def goals(request):
    return render(request, 'myapp/goals.html')

def help(request):
    return render(request, 'myapp/help.html')


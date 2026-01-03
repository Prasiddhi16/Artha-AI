from django.shortcuts import render

def home(request):
    return render(request, 'myapp/home.html')

def analytics(request):
    return render(request, 'myapp/analytics.html')

def budget(request):
    return render(request, 'myapp/budget.html')

def review(request):
    return render(request, 'myapp/review.html')

def goals(request):
    return render(request, 'myapp/goals.html')

def help(request):
    return render(request, 'myapp/help.html')

def profile(request):
    return render(request, 'myapp/profile.html')

def signin(request):
    return render(request, 'myapp/signin.html')

def signup(request):
    return render(request, 'myapp/signup.html')

def chatbot(request):
    return render(request, 'myapp/chatbot.html')


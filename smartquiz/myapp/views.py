from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'register.html')
        
        # Create user
        User.objects.create_user(username=username, password=password)
        messages.success(request, "User registered successfully! You can login now.")
        return redirect('/login/')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('/home/')
        else:
            messages.error(request, "Invalid username or password!")
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')

# Subject views
def science(request):
    return render(request, 'science.html')

def history(request):
    return render(request, 'history.html')

def maths(request):
    return render(request, 'maths.html')

def sports(request):
    return render(request, 'sports.html')

def profile(request):
    return render(request, 'profile.html')


def result(request):
    # Get score and subject from URL parameters
    score = request.GET.get('score', 0)
    subject = request.GET.get('subject', '-')
    
    # Optional: get username from session (assuming login sets it in session)
    username = request.session.get('username', 'Guest')

    # Determine motivational message
    score_int = int(score)
    if score_int == 5:
        msg = "🏆 Excellent! You nailed it!"
    elif score_int >= 3:
        msg = "👏 Good job! Keep practicing!"
    else:
        msg = "💪 Don't give up! Try again!"

    context = {
        'username': username,
        'subject': subject,
        'score': score,
        'message': msg
    }

    return render(request, 'result.html', context)
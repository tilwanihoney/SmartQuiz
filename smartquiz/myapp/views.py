from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Max, Avg


from .models import Subject, Question, QuizResult


def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    subjects = Subject.objects.all()
    return render(request, 'home.html', {"subjects": subjects})

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'register.html')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "User registered successfully! You can login now.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('welcome')


# ---------- QUIZ LOGIC ----------

def start_quiz(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to play the quiz.")
        return redirect('login')

    if request.method != "POST":
        return redirect('home')

    subject_id = request.POST.get('subject')
    if not subject_id:
        messages.error(request, "Please choose a subject.")
        return redirect('home')

    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        messages.error(request, "Invalid subject selected.")
        return redirect('home')

    questions = list(Question.objects.filter(subject=subject))
    if not questions:
        messages.error(request, "No questions available for this subject yet.")
        return redirect('home')

    random.shuffle(questions)
    questions = questions[:5]   # ask max 5

    request.session['quiz_question_ids'] = [q.id for q in questions]
    request.session['quiz_subject_id'] = subject.id

    return render(request, 'quiz.html', {
        "subject": subject,
        "questions": questions,
        "username": request.user.username,
    })


def submit_quiz(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method != "POST":
        return redirect('home')

    question_ids = request.session.get('quiz_question_ids', [])
    subject_id = request.session.get('quiz_subject_id', None)

    if not question_ids:
        messages.error(request, "Quiz session expired. Please start again.")
        return redirect('home')

    questions = Question.objects.filter(id__in=question_ids)
    subject = Subject.objects.filter(id=subject_id).first()

    score = 0
    for q in questions:
        selected = request.POST.get(f"question_{q.id}")
        if selected and selected == q.correct_option:
            score += 1

    result = QuizResult.objects.create(
        user=request.user,
        subject=subject,
        score=score,
        total_questions=questions.count()
    )

    if score == questions.count():
        msg = "🏆 Excellent! You nailed it!"
    elif score >= questions.count() // 2:
        msg = "👏 Good job! Keep practicing!"
    else:
        msg = "💪 Don't give up! Try again!"

    return render(request, 'result.html', {
        "result": result,
        "message": msg,
        "username": request.user.username,
    })



def leaderboard(request):
    results = QuizResult.objects.all().order_by('-score', '-created_at')[:20]  # Top 20

    return render(request, "leaderboard.html", {
        "leaderboard": results,
    })




def profile(request):
    # get all results for this logged-in user
    results = QuizResult.objects.filter(user=request.user).order_by('-created_at')

    # highest score for this user (optional, can remove if you don't want)
    best_score = results.aggregate(Max('score'))['score__max'] or 0

    context = {
        'results': results,
        'best_score': best_score,
    }
    return render(request, 'profile.html', context)
























 
 
 
 
 

 
 
 
 

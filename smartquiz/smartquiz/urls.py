from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('result/',views.result,name='result'),
    path('profile/',views.profile,name='profile'),

    # Subject pages
    path('science/', views.science, name='science'),
    path('history/', views.history, name='history'),
    path('maths/', views.maths, name='maths'),
    path('sports/', views.sports, name='sports'),
]

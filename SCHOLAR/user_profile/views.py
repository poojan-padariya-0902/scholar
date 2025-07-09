from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        faculty = Faculty.objects.all().order_by('-id')
        caurse = Caurse.objects.all().order_by('-id')
        context = {
            'user': user,
            'faculty' : faculty,
            'caurse': caurse,
        }
        return render(request, 'index.html', context)
    return render(request, 'index.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('index')
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('index')
        password = request.POST.get('password')

        user = User.objects.create(first_name=first_name,last_name=last_name, email=email, username=username, password=password)
        user.set_password(password)  # Hash the password
        user.save()

        send_mail(
            subject='Welcome to SCHOLAR',
            message=f'Hello {first_name},\n\nThank you for registering at SCHOLAR. You can now log in using your credentials.\n\nBest regards,\nSCHOLAR Team',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        send_mail(
            subject='New User Registration',
            message=f'New user registered:\n\nFirst Name: {first_name}\nLast name: {last_name}\nUsername: {username}\nEmail: {email}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  # Ensure you have an ADMIN_EMAIL setting
            fail_silently=False,
        )

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('index')
    
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('index')

    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')
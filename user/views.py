from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import User


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email == '' or password == '':
            messages.error(request, 'Please fill out all fields')
            return redirect('login')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You`ve successfully logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'user/login.html')


def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if email == '' or password == '' or confirm_password == '':
            messages.error(request, 'Please fill out all fields')
            return redirect('signup')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exist')
            return redirect('signup')

        user = User.objects.create_user(email=email, password=password)
        user.save()

        login(request, user)
        messages.success(request, 'You have successfully registered')

        return redirect('index')


    return render(request, 'user/register.html')


def index(request):
    return render(request, 'user/index.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('index')



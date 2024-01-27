from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import User


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # re-initialising the storage to clear it
        request._messages = messages.storage.default_storage(request)

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

        # re-initialising the storage to clear it
        request._messages = messages.storage.default_storage(request)

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


@login_required
def profile(request):
    user = request.user
    return render(request, 'user/profile.html', {'user': user})


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.birthday = request.POST['birthday']
        user.sex = request.POST['sex']
        user.save()
        return redirect('profile')

    return render(request, 'user/edit_profile.html', {'user': request.user})

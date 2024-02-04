from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View

from .models import User


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

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


class SignupView(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

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


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out')
        return redirect('index')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'user/profile.html', {'user': user})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'user/edit_profile.html', {'user': user})

    def post(self, request):
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.birthday = request.POST.get('birthday')
        user.sex = request.POST.get('sex')
        user.save()

        return redirect('profile')

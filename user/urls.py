from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login_view, name='login' ),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit_profile', views.edit_profile, name='edit_profile')
]

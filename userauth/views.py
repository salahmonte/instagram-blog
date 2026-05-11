from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from insta.models import Post   # adjust app name if different


# Create your views here.

def Registerview(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, f"User with username '{username}' already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, f"User with email '{email}' already exists")

        if password != password1:
            user_data_has_error = True
            messages.error(request, "Passwords do not match")

        if not user_data_has_error:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            new_user.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')

        return redirect('register')

    return render(request, 'userauth/register.html')


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'userauth/login.html')


def LogoutView(request):
    logout(request)
    return redirect('instahome')
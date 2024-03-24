from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required

def home_view(request):
    if request.user.id:
        if request.user.is_superuser:
            return redirect('/ticket/dashboard')
        else:
            return redirect("/ticket/list/")
    return render(request, 'home.html')

def not_auth_view(request):
    return render(request, 'not_auth.html')
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/ticket/dashboard')
                else:
                    return redirect("/ticket/list/")
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account created for {username}. You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

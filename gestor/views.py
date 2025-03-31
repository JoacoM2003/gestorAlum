from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered")
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    else:
        return render(request, 'sign/signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'sign/signin.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('signin')

@login_required
def signout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')
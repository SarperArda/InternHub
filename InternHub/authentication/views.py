from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
@login_required(login_url='login')
def home_page(request):
    return render(request, 'authentication/home.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Incorrect username or password try again.")
            return redirect('login')

    return render(request, 'authentication/login.html')


def logout_page(request):
    logout(request)
    return render(request, 'authentication/logout.html')

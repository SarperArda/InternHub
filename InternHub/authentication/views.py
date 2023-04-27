from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'authentication/home.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.success(request, ("Incorrect username or password try again."))
            return redirect('login')

    return render (request,'authentication/login.html')

def LogoutPage(request):
    logout(request)
    return render(request, 'authentication/logout.html')
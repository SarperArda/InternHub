from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        user_id = request.POST.get('id')
        form = LoginForm(request.POST)
        password = request.POST.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid email address or password.'
    else:
        error_message = None

    return render(request, 'main/login.html', {"form": form,
                                               'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('login')

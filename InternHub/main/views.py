from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import LoginForm


def login_view(request):
    form = LoginForm()
    error_message = None
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        form = LoginForm(request.POST)
        password = request.POST.get('password')

        try: 
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            error_message = 'User does not exist.'
            user = None

        if user is not None:
            authenticated_user = authenticate(request,user_id=user_id, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')
            else:
                error_message = 'Invalid id or password.'

    return render(request, 'main/login.html', {'form': form,
                                               'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('login')

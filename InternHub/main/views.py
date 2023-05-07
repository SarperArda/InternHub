from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Announcement
from .forms import LoginForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import AnnouncementForm
from django.views.generic.edit import FormView
from .decorators import allowed_users
from django.utils.decorators import method_decorator

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
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
            authenticated_user = authenticate(request, user_id=user_id, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')
            else:
                error_message = 'Invalid id or password.'

    return render(request, 'main/login.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('login')


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = ''

    def get(self, request):
        announcements = Announcement.objects.all().order_by("-date")
        return render(request, 'main/home.html', {'announcements': announcements})
    

class AnnouncementView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    redirect_field_name = '/announcement/'
    form_class = AnnouncementForm
    template_name = 'main/announcement.html'
    success_url = '/'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

    @method_decorator(allowed_users(['SUPERUSER', 'DEAN', 'CHAIR', 'DEPARTMENT_SECRETARY']))
    def dispatch(self, *args, **kwargs):
        print("Hey")
        return super().dispatch(*args, **kwargs)

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return self.request.user.role in self.allowed_roles

    def handle_no_permission(self):
        return redirect('users:forbidden')


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(
            self.request,
            user_id=form.cleaned_data['user_id'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(self.request, user)
            return redirect('main:home')
        else:
            form.add_error(None, 'Invalid id or password.')
            return self.form_invalid(form)
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')
    
class ForbiddenView(View):
    def get(self, request):
        return render(request, 'users/forbidden.html')

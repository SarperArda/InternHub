from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView

from reports.models import Internship
from .forms import LoginForm


# Create your views here.
class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return self.request.user.role in self.allowed_roles

    def handle_no_permission(self):
        return redirect('users:forbidden')


class UserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.role in ['STUDENT', 'INSTRUCTOR']:
            try:
                internship = Internship.objects.get(id=self.kwargs['pk'])
                user_id = self.request.user.user_id
                # Only pass if user is the student or instructor associated with the Internship
                return user_id == internship.student.user_id or user_id == internship.instructor.user_id
            except Internship.DoesNotExist:
                return False
        else:
            # If user's role is neither 'student' nor 'instructor', they pass automatically
            return True

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
            form.add_error(None, 'Invalid ID or password.')
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')


class ForbiddenView(View):
    def get(self, request):
        return render(request, 'users/forbidden.html')

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.decorators import allowed_users
from django.utils.decorators import method_decorator

from .forms import AnnouncementForm
# Create your views here.
class MakeAnnouncementView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    form_class = AnnouncementForm
    template_name = 'announcements/announcement.html'
    success_url = '/'
    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.save()
        return super().form_valid(form)
    

    @method_decorator(allowed_users(['SUPERUSER', 'DEAN', 'CHAIR', 'DEPARTMENT_SECRETARY']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
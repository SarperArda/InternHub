from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from users.views import RoleRequiredMixin
from .forms import AnnouncementForm


class MakeAnnouncementView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    login_url = '/login/'
    form_class = AnnouncementForm
    template_name = 'announcements/announcement.html'
    success_url = '/'
    allowed_roles = ['SUPERUSER', 'DEAN', 'CHAIR', 'DEPARTMENT_SECRETARY']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['full_name'] = str(self.request.user)
        context['user'] = user
        context['check'] = True
        return context

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.save()
        return super().form_valid(form)

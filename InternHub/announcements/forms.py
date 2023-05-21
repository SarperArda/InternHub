from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        labels = {
            "title": "Your Title",
            "content": "Your Announcement"
        }
        error_messages = {
            "title": {
                "required": "Please enter a title."
            },
            "content": {
                "required": "Please enter an announcement."
            }
        }

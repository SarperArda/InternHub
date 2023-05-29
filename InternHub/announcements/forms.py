from django import forms

from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        labels = {
            "title": "Announcement Title",
            "content": "Announcement Content"
        }
        error_messages = {
            "title": {
                "required": "Please enter a title."
            },
            "content": {
                "required": "Please enter a content."
            }
        }

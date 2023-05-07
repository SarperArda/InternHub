from django import forms
from .models import Announcement

class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=8,
        widget=forms.TextInput(attrs={'placeholder': 'Bilkent ID'}),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label=''
    )

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

    

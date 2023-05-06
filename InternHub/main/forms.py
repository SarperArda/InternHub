from django import forms


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

    

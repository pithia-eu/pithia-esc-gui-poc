from django import forms

class LoginForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

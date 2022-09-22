from django.shortcuts import render

from common.forms import LoginForm

def index(request):
    return render(request, 'index.html', {
        'title': 'PITHIA e-Science Centre Home',
    })

def login(request):
    form = LoginForm()
    return render(request, 'login.html', {
        'title': 'Enter password',
        'form': form
    })
import environ
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Initialise environment variables
env = environ.Env()

from common.forms import LoginForm

def index(request):
    return render(request, 'index.html', {
        'title': 'PITHIA e-Science Centre Home',
    })

def login(request):
    if 'is_authorised' in request.session and request.session['is_authorised'] == True:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if request.POST.get('password') != env('ESC_PASSWORD'):
                messages.error(request, 'Password is incorrect.')
                if request.GET.get('next', '') != '':
                    return HttpResponseRedirect('%s?next=%s' % (reverse('login'), request.GET.get('next', '')))
                return HttpResponseRedirect(reverse('login'))
            request.session['is_authorised'] = True
            if request.GET.get('next', '') != '':
                return HttpResponseRedirect(request.GET.get('next', ''))
            return HttpResponseRedirect(reverse('home'))
    form = LoginForm()
    return render(request, 'login.html', {
        'title': 'Enter password',
        'form': form,
        'next': request.GET.get('next', '')
    })

def logout(request):
    if 'is_authorised' in request.session:
        del request.session['is_authorised']
    return HttpResponseRedirect(reverse('login'))

def index_admin(request):
    return render(request, 'index.html', {
        'title': 'Admin Dashboard',
    })

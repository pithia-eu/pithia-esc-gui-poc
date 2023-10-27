import environ
import hashlib
import os
from django.contrib import messages
from django.http import (
    FileResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse

from common.forms import LoginForm
from pithiaesc.settings import BASE_DIR

# Initialise environment variables
env = environ.Env()


def index(request):
    return render(request, 'index.html', {
        'title': 'PITHIA e-Science Centre',
    })

def login(request):
    if 'is_authorised' in request.session and request.session['is_authorised'] == True:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
            if hashed_password != env('ESC_PASSWORD'):
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

def resource_registration_user_guide(request):
    try:
        return FileResponse(open(os.path.join(BASE_DIR, 'resource_management', 'PITHIA-NRF Data Registration User Guide.pdf'), 'rb'), content_type='application/pdf')
    except IOError:
        return HttpResponseNotFound('The data resource registration guide was not found.')
    
def terms_of_use(request):
    return render(request, 'terms-of-use.html', {
        'title': 'PITHIA e-Science Centre Acceptable Use Policy and Conditions of Use'
    })

def privacy_policy(request):
    return render(request, 'privacy-policy.html', {
        'title': 'PITHIA e-Science Centre Privacy Policy'
    })

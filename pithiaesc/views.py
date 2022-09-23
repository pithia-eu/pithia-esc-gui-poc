from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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
            request.session['is_authorised'] = True
            print("request.GET.get('next', '')", request.GET.get('next', ''))
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
    del request.session['is_authorised']
    return HttpResponseRedirect(reverse('home'))
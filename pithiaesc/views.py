import environ
import hashlib
import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from common.forms import LoginForm

# Initialise environment variables
env = environ.Env()


from user_management.services import (
    CREATION_URL_BASE,
    get_user_info,
    verify_if_part_of_an_organisation,
)

def logout(request):
    # Send a GET request to the EGI Check-in Logout endpoint
    ID_TOKEN_HINT = request.META.get('OIDC_id_token')
    logout_response = requests.get(f'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/logout?id_token_hint={ID_TOKEN_HINT}')
    
    # TEST: Redirect straight to the EGI Check-in logout page.
    # return HttpResponseRedirect(f'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/logout?id_token_hint={ID_TOKEN_HINT}')
    
    # Verify EGI Check-in logout was successful by checking for an
    # error from the UserInfo API.
    
    ACCESS_TOKEN = request.META.get('OIDC_access_token')
    user_info = get_user_info(ACCESS_TOKEN)
    error_in_user_info = 'error' in user_info
    # TODO: maybe add some additional actions after
    # logout has been verified.

    return render(request, 'index.html', {
        'title': f'PITHIA e-Science Centre Home',
        'logout_response': logout_response,
        'ID_TOKEN_HINT': ID_TOKEN_HINT,
        'error_in_user_info': error_in_user_info,
    })

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
    ACCESS_TOKEN = request.META.get('OIDC_access_token')
    user_info = get_user_info(ACCESS_TOKEN)
    is_part_of_an_organisation = verify_if_part_of_an_organisation(user_info)

    return render(request, 'index.html', {
        'title': 'Admin Dashboard',
        'is_part_of_an_organisation': is_part_of_an_organisation,
        'create_perun_organisation_url': CREATION_URL_BASE,
    })

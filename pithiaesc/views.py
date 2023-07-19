import environ
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode

from user_management.services import CREATION_URL_BASE

# Initialise environment variables
env = environ.Env()


from user_management.services import (
    CREATION_URL_BASE,
    remove_login_session_variables,
)

def logout(request):
    # Remove relevant session variables
    remove_login_session_variables(request)

    absolute_home_page_uri = request.build_absolute_uri(reverse("home"))
    return HttpResponseRedirect(f'/authorised/?{urlencode({"logout": absolute_home_page_uri})}')

def index(request):
    return render(request, 'index.html', {
        'title': 'PITHIA-NRF e-Science Centre',
        'create_institution_url': CREATION_URL_BASE,
    })

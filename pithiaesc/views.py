import environ
from django.http import HttpResponseRedirect
import os
from django.http import (
    FileResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode

from pithiaesc.settings import BASE_DIR
from user_management.services import CREATION_URL_BASE

# Initialise environment variables
env = environ.Env()


from user_management.services import (
    CREATION_URL_BASE,
    remove_login_session_variables,
)

def logout(request):
    # Remove relevant session variables
    remove_login_session_variables(request.session)

    absolute_home_page_uri = request.build_absolute_uri(reverse("home"))
    return HttpResponseRedirect(f'/authorised/?{urlencode({"logout": absolute_home_page_uri})}')

def index(request):
    return render(request, 'index.html', {
        'title': 'PITHIA-NRF e-Science Centre',
        'create_institution_url': CREATION_URL_BASE,
    })

def resource_registration_user_guide(request):
    try:
        return FileResponse(open(os.path.join(BASE_DIR, 'resource_management', 'PITHIA-NRF Data Registration User Guide.pdf'), 'rb'), content_type='application/pdf')
    except IOError:
        return HttpResponseNotFound('The data resource registration guide was not found.')

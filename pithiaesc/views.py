import environ
import requests
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode

# Initialise environment variables
env = environ.Env()


from user_management.services import (
    CREATION_URL_BASE,
    get_user_info,
    remove_login_session_variables,
)

@require_POST
def logout(request):
    # Remove relevant session variables
    remove_login_session_variables(request)

    return HttpResponseRedirect(f'{request.build_absolute_uri("authorised/")}?{urlencode({"logout": request.build_absolute_uri(reverse("home"))})}')

    # Send a GET request to the EGI Check-in Logout endpoint
    ID_TOKEN_HINT = request.META.get('OIDC_id_token')
    logout_response = requests.get(f'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/logout?id_token_hint={ID_TOKEN_HINT}')

    # TEST: Verify logout was successful by checking for success
    # status code in response.
    # print('logout_response', logout_response)
    
    # TEST: Redirect straight to the EGI Check-in logout page.
    # return HttpResponseRedirect(f'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/logout?id_token_hint={ID_TOKEN_HINT}')
    
    # TEST: Verify EGI Check-in logout was successful by checking for an
    # error from the UserInfo API.
    # ACCESS_TOKEN = request.META.get('OIDC_access_token')
    # try:
    #     user_info = get_user_info(ACCESS_TOKEN)
    #     error_in_user_info = 'error' in user_info
    # except:
    #     pass

    return HttpResponseRedirect(reverse('home'))

def index(request):
    return render(request, 'index.html', {
        'title': 'PITHIA e-Science Centre Home',
    })

def index_admin(request):
    return render(request, 'index.html', {
        'title': 'Admin Dashboard',
        'create_perun_organisation_url': CREATION_URL_BASE,
    })

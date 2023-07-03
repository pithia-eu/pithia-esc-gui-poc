import json
import requests

from django.shortcuts import render

from user_management.services import (
    CREATION_URL_BASE,
    get_user_info,
)

def logout(request):
    # Send a GET request to the EGI Check-in Logout endpoint
    ID_TOKEN_HINT = request.META.get('OIDC_id_token')
    logout_response = requests.get(f'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/logout?id_token_hint={ID_TOKEN_HINT}')
    
    # TEST: Redirect straight to the EGI Check-in logout page.
    # return HttpResponseRedirect(f'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/logout?id_token_hint={ID_TOKEN_HINT}')
    
    # Verify EGI Check-in logout was successful by checking for an
    # error from the UserInfo API.
    url = 'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/userinfo'
    ACCESS_TOKEN = request.META.get('OIDC_access_token')
    user_info_response = get_user_info(url, ACCESS_TOKEN)
    user_info = json.loads(user_info_response.text)
    error_in_user_info = 'error' in user_info

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

def index_admin(request):
    return render(request, 'index.html', {
        'title': 'Admin Dashboard',
        'create_perun_organisation_url': CREATION_URL_BASE,
    })
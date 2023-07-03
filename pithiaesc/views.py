import requests

from django.shortcuts import render

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

def index_admin(request):
    ACCESS_TOKEN = request.META.get('OIDC_access_token')
    user_info = get_user_info(ACCESS_TOKEN)
    is_part_of_an_organisation = verify_if_part_of_an_organisation(user_info)

    return render(request, 'index.html', {
        'title': 'Admin Dashboard',
        'is_part_of_an_organisation': is_part_of_an_organisation,
        'create_perun_organisation_url': CREATION_URL_BASE,
    })
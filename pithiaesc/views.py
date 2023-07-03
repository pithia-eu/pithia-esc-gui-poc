import json
import requests

from django.shortcuts import render

from user_management.services import (
    get_user_info,
)

def logout(request):
    ID_TOKEN_HINT = request.META.get('OIDC_id_token')
    # Logout
    logout_response = requests.get(f'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/logout?id_token_hint={ID_TOKEN_HINT}')
#    return HttpResponseRedirect(f'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/logout?id_token_hint={ID_TOKEN_HINT}')
    url = 'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/userinfo'
    request_meta = request.META.items()
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
        'create_perun_organisation_url': 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizationRequests',
    })
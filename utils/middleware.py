"""
Implementation creditation: https://stackoverflow.com/a/2164224/10640126
"""

import re
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse_lazy

from user_management.services import get_user_info

class LoginMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        access_token = request.META.get('OIDC_access_token')
        if access_token is not None:
            # Store user info in session to minimise
            # calls to the UserInfo API.
            user_info = get_user_info(access_token)
            request.session['is_logged_in'] = True
            request.session['eduperson_entitlement'] = user_info.get('eduperson_entitlement')
            request.session['email'] = user_info.get('email')

        return response

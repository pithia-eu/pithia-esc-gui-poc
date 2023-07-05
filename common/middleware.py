"""
Implementation creditation: https://stackoverflow.com/a/2164224/10640126
"""

import re

from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse_lazy

class LoginMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response
        self.required = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # No need to process URLs if user already logged in
        if 'is_logged_in' in request.session and request.session['is_logged_in'] == True:
            return response

        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path):
                return response

        # Requests matching a restricted URL pattern return the login view.=
        for url in self.required:
            if url.match(request.path):
                return HttpResponseRedirect('%s?next=%s' % (reverse_lazy('login'), request.get_full_path()))

        return response
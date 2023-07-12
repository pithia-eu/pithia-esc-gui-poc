from django.http import HttpResponseRedirect
from django.urls import reverse

from user_management.services import (
    get_user_info,
    get_highest_subgroup_of_each_institution_for_logged_in_user,
    remove_login_session_variables,
)

class LoginMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def _get_user_info_and_set_login_variables(self, request, access_token):
        user_info = get_user_info(access_token)
        if 'error' in user_info:
            remove_login_session_variables(request)
            return HttpResponseRedirect(reverse('home'))

        # Store user info in session to minimise
        # calls to the UserInfo API.
        request.session['OIDC_access_token'] = access_token
        request.session['is_logged_in'] = True
        try:
            request.session['user_institution_subgroups'] = get_highest_subgroup_of_each_institution_for_logged_in_user(user_info['eduperson_entitlement'])
        except KeyError:
            request.session['user_institution_subgroups'] = []
        request.session['user_email'] = user_info.get('email')
        request.session['user_given_name'] = user_info.get('given_name')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Verify if the user is logged in or not.

        # Check if an OIDC_access_token exists in
        # request.META.
        access_token_in_headers = request.META.get('OIDC_access_token')
        access_token_in_session = request.session.get('OIDC_access_token')

        if access_token_in_headers:
            # If an OIDC_access_token exists in the headers,
            # keep an up-to-date copy of it in the session.
            # This ensures that any outdated tokens in the
            # session are overwritten with each request.
            request.session['OIDC_access_token'] = access_token_in_headers
            access_token_in_session = access_token_in_headers

        if access_token_in_session is None:
            # If there isn't one in the session, can probably
            # just assume that the user is logged out.
            remove_login_session_variables(request)
            if '/authorised' in request.path:
                return HttpResponseRedirect(reverse('home'))
        else:
            self._get_user_info_and_set_login_variables(request, access_token_in_session)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

class LoginSessionInstitutionMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        exempt_paths = [
            reverse('logout'),
            reverse('list_joinable_perun_organisations'),
            reverse('choose_perun_organisation_subgroup_for_session'),
        ]
        # Join an institution subgroup page cannot be
        # resolved with reverse, so have to use
        # another method to match the current
        # path with an exempt path.
        is_current_path_exempt = any([p in request.path for p in exempt_paths])
        is_institution_for_login_session_required = (
            request.session.get('is_logged_in') is True
            and 'institution_for_login_session' not in request.session
            and 'subgroup_for_login_session' not in request.session
        )
        request.session['is_institution_for_login_session_required'] = is_institution_for_login_session_required

        if (is_institution_for_login_session_required
            and not is_current_path_exempt):
            return HttpResponseRedirect(reverse('choose_perun_organisation_subgroup_for_session'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

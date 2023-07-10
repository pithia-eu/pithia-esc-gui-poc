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
        request.session['user_institution_subgroups'] = get_highest_subgroup_of_each_institution_for_logged_in_user(user_info.get('eduperson_entitlement'))
        request.session['user_email'] = user_info.get('email')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # Verify if the user is logged in or not.

        # Check if an OIDC_access_token exists in
        # request.META.
        access_token = request.META.get('OIDC_access_token')
        access_token_copy = request.session.get('OIDC_access_token')

        if access_token:
            # If an OIDC_access_token exists, check that
            # it's matching with the one in the session.

            if access_token == access_token_copy:
                # If the OIDC_access_token in the headers
                # is the same as the one in the session,
                # all the login variables should be set
                # in the session.
                return response

            # If there isn't an OIDC_access_token in the
            # session, or, if there is an OIDC_access_token
            # in the session, assume that it's outdated and
            # copy the OIDC_access_token from the headers to
            # the session.
            request.session['OIDC_access_token'] = access_token

            # Once the session OIDC_access_token has been
            # overwritten, call the User Info API.
            self._get_user_info_and_set_login_variables(request, access_token)
        else:
            # If an OIDC_access_token is not in the headers
            # (e.g., the user is accessing a non-authorised
            # URL), use the copy in the session.

            if access_token_copy is None:
                # If there isn't one in the session, can probably
                # just assume that the user is logged out.
                remove_login_session_variables(request)
                return response

            # If there is one in the session, verify it is
            # still valid by calling the User Info API. If
            # it is not valid, delete the login vars and
            # log the user out.
            self._get_user_info_and_set_login_variables(request, access_token_copy)

        return response

class LoginSessionInstitutionMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if (reverse('choose_perun_organisation_subgroup_for_session') != request.path
            and reverse('logout') != request.path
            and 'institution_for_login_session' not in request.session
            and 'subgroup_for_login_session' not in request.session):
            return HttpResponseRedirect(reverse('choose_perun_organisation_subgroup_for_session'))

        return response

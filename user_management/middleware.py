from django.http import HttpResponseRedirect
from django.urls import reverse

from common.forms import InstitutionForLoginSessionForm
from user_management.services import (
    delete_institution_for_login_session,
    get_user_info,
    get_highest_subgroup_of_each_institution_for_logged_in_user,
    get_institution_id_for_login_session,
    get_institution_memberships_of_logged_in_user,
    get_subgroup_id_for_login_session,
    remove_login_session_variables,
    set_institution_for_login_session,
)


class LoginMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def _get_user_info_and_set_login_variables(self, request, access_token):
        user_info = get_user_info(access_token)
        if 'error' in user_info:
            remove_login_session_variables(request.session)
            return HttpResponseRedirect(reverse('home'))

        # Store user info in session to minimise
        # calls to the UserInfo API.
        request.session['OIDC_access_token'] = access_token
        request.session['is_logged_in'] = True
        try:
            request.session['user_institution_subgroups'] = get_highest_subgroup_of_each_institution_for_logged_in_user(user_info['eduperson_entitlement'])
        except KeyError:
            request.session['user_institution_subgroups'] = {}
        request.session['user_id'] = request.META.get('OIDC_CLAIM_sub')
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
            remove_login_session_variables(request.session)
            if '/authorised' in request.path:
                return HttpResponseRedirect(reverse('home'))
        else:
            self._get_user_info_and_set_login_variables(request, access_token_in_session)

        # Check if the user is still a member of the
        # institution they have logged in with. If not,
        # perform the appropriate action.
        logged_in_institution_id = get_institution_id_for_login_session(request.session)
        logged_in_institution_subgroup_id = get_subgroup_id_for_login_session(request.session)
        user_memberships = get_institution_memberships_of_logged_in_user(request.session)
        if (logged_in_institution_id is not None
            and logged_in_institution_id not in user_memberships):
            delete_institution_for_login_session(request.session)
        elif (logged_in_institution_id is not None
            and user_memberships.get(logged_in_institution_id) != logged_in_institution_subgroup_id):
            # If the user's permissions changed whilst
            # they are logged, update the user's
            # permission level automatically.
            set_institution_for_login_session(
                request.session,
                logged_in_institution_id,
                user_memberships.get(logged_in_institution_id)
            )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

class InstitutionSelectionMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        try:
            user_memberships = get_institution_memberships_of_logged_in_user(request.session)
            if len(user_memberships.keys()) == 1:
                set_institution_for_login_session(
                    request.session,
                    list(user_memberships.keys())[0],
                    list(user_memberships.values())[0]
                )
        except AttributeError:
            pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

class InstitutionSelectionFormMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        try:
            user_memberships = get_institution_memberships_of_logged_in_user(request.session)
            institution_choices = [(f'{institution}:{subgroup}', institution) for institution, subgroup in user_memberships.items()]
            institution_selection_form = InstitutionForLoginSessionForm(institution_choices, initial={'next': request.path})
            request.institution_selection_form = institution_selection_form
        except AttributeError:
            pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
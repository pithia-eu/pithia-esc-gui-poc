import logging
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


logger = logging.getLogger(__name__)


class LoginMiddleware(object):
    ACCESS_TOKEN_DICT_KEY = 'OIDC_access_token'
    USER_INSTITUTION_SUBGROUPS_DICT_KEY = 'user_institution_subgroups'

    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    # User info
    def _set_user_info_related_session_variables(self, request, user_info):
        # Configuring login session variables
        # Store user info in session to minimise
        # calls to the User Info API.
        request.session['is_logged_in'] = True
        try:
            request.session[self.USER_INSTITUTION_SUBGROUPS_DICT_KEY] = get_highest_subgroup_of_each_institution_for_logged_in_user(user_info['eduperson_entitlement'])
        except KeyError:
            request.session[self.USER_INSTITUTION_SUBGROUPS_DICT_KEY] = {}
        request.session['user_given_name'] = user_info.get('given_name')

    def _verify_access_token_and_set_user_info_session_variables(self, request, access_token):
        # Access token verification
        user_info = get_user_info(access_token)
        if 'error' in user_info:
            # The User Info API will return an error if
            # the access token has been invalidated.
            raise Exception(f'An error was found in/whilst processing the user info response.')
        self._set_user_info_related_session_variables(request, user_info)

    # Request META variables
    def _set_request_meta_variable_in_session_if_possible(self, request, key_in_request_meta: str, key_in_session: str = None):
        request_meta_variable = request.META.get(key_in_request_meta)
        if not request_meta_variable:
            return None
        if not key_in_session:
            request.session[key_in_request_meta] = request_meta_variable
            return None
        request.session[key_in_session] = request_meta_variable
        return None

    def _set_request_meta_variables_for_login_session_if_possible(self, request):
        """The access token is stored in the session to allow the login
        status to be checked when accessing a non-protected route, as
        it's only present in the request headers when accessing a protected
        route.
        The token in the session is updated whenever it's present in the
        request headers to ensure any outdated session access tokens are
        overwritten.
        """
        self._set_request_meta_variable_in_session_if_possible(request, self.ACCESS_TOKEN_DICT_KEY)
        self._set_request_meta_variable_in_session_if_possible(request, 'OIDC_CLAIM_sub', key_in_session='user_id')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        try:
            # Verify if the user is logged in or not.
            # Check if an OIDC_access_token exists in
            # request.META, and perform the appropriate
            # action.
            self._set_request_meta_variables_for_login_session_if_possible(request)


            # The access token should always be retrieved from the
            # session. This is because the access token may not
            # always be present in the headers.
            access_token_in_session = request.session.get(self.ACCESS_TOKEN_DICT_KEY)
            if not access_token_in_session:
                # Access token is not present, so assume that the
                # user is logged out.
                remove_login_session_variables(request.session)
                if '/authorised' in request.path:
                    return HttpResponseRedirect(reverse('home'))
            else:
                self._verify_access_token_and_set_user_info_session_variables(request, access_token_in_session)

            
            # Check if the user is still a member of the institution
            # they are logged in with. If not, perform the appropriate
            # action.
            institution_id_logged_in_with = get_institution_id_for_login_session(request.session)
            memberships_of_logged_in_user = get_institution_memberships_of_logged_in_user(request.session)
            is_user_still_member_of_institution_logged_in_with = (
                # User is logged in with an institution
                institution_id_logged_in_with is not None
                # User is a member of an institution
                and memberships_of_logged_in_user is not None
                # User is still a member of the institution they are logged in with
                and institution_id_logged_in_with in memberships_of_logged_in_user
            )

            # The logged in user's memberships should be updated with
            # every request, so it can be used to verify if a user's
            # authorisation level (decided by the highest level of
            # subgroup they are currently in), is still valid.
            institution_subgroup_id_logged_in_with = get_subgroup_id_for_login_session(request.session)
            is_user_authorisation_level_correct = (
                institution_subgroup_id_logged_in_with is not None
                and memberships_of_logged_in_user is not None
                # Subgroup the user is logged in with still matches
                # the information from the User Info API.
                and institution_subgroup_id_logged_in_with == memberships_of_logged_in_user.get(institution_id_logged_in_with)
            )

            if (institution_id_logged_in_with is not None
                and not is_user_still_member_of_institution_logged_in_with):
                delete_institution_for_login_session(request.session)
            elif (institution_id_logged_in_with is not None
                and not is_user_authorisation_level_correct):
                # If the user's permissions changed whilst
                # they are logged in, update the user's
                # permission level here.
                set_institution_for_login_session(
                    request.session,
                    institution_id_logged_in_with,
                    memberships_of_logged_in_user.get(institution_id_logged_in_with)
                )
        except Exception:
            logger.exception('An unexpected error occurred during authentication.')
            remove_login_session_variables(request.session)
            if '/authorised' in request.path:
                return HttpResponseRedirect(reverse('home'))

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
            memberships_of_logged_in_user = get_institution_memberships_of_logged_in_user(request.session)
            if len(memberships_of_logged_in_user.keys()) == 1:
                set_institution_for_login_session(
                    request.session,
                    list(memberships_of_logged_in_user.keys())[0],
                    list(memberships_of_logged_in_user.values())[0]
                )
        except AttributeError:
            pass
        except Exception:
            logger.exception('An unexpected error occurred whilst trying to apply the user\'s login session institution.' )

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
            memberships_of_logged_in_user = get_institution_memberships_of_logged_in_user(request.session)
            institution_choices = [(f'{institution}:{subgroup}', institution) for institution, subgroup in memberships_of_logged_in_user.items()]
            institution_selection_form = InstitutionForLoginSessionForm(
                institution_choices=institution_choices,
                initial={'next': request.path}
            )
            request.institution_selection_form = institution_selection_form
        except AttributeError:
            # session.get('memberships_of_logged_in_user') will raise an AttributeError if
            # user memberships have not been stored in the session yet.
            pass
        except Exception:
            logger.exception('An unexpected error occurred whilst trying to setup the login institution selection form.' )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
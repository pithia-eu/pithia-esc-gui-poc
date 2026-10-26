import logging
from django.http import HttpResponseRedirect
from django.urls import reverse

from common.forms import InstitutionForLoginSessionForm
from user_management.services import (
    delete_institution_for_login_session,
    query_user_info_api,
    get_highest_subgroup_of_each_institution_for_logged_in_user,
    get_institution_id_for_login_session,
    get_institution_memberships_of_logged_in_user,
    get_subgroup_id_for_login_session,
    remove_login_session_variables,
    set_institution_for_login_session,
)


logger = logging.getLogger(__name__)


class LoginMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    # User info
    def get_user_info(self, request, access_token: str):
        # Access token verification
        user_info = query_user_info_api(access_token)
        if 'error' in user_info:
            return None
        return user_info

    def copy_user_privilege_info_to_session(self, request, user_info: dict):
        USER_INSTITUTION_SUBGROUPS_DICT_KEY = 'user_institution_subgroups'
        try:
            request.session[USER_INSTITUTION_SUBGROUPS_DICT_KEY] = get_highest_subgroup_of_each_institution_for_logged_in_user(user_info['eduperson_entitlement'])
        except KeyError:
            request.session[USER_INSTITUTION_SUBGROUPS_DICT_KEY] = {}

    def copy_user_given_name_to_session(self, request, user_info: dict):
        request.session['user_given_name'] = user_info.get('given_name')
        

    def logout_and_return_response(self, request):
        remove_login_session_variables(request.session)
        if '/authorised' not in request.path:
            # If not in a protected path, no need for further
            # login session management, just carry on with the
            # request.
            return self.get_response(request)
        return HttpResponseRedirect(reverse('home'))

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Check that the access token is still valid. First, check that
        # there is an access token to check. If there isn't one, perform
        # a logout.
        OIDC_ACCESS_TOKEN_KEY = 'OIDC_access_token'
        access_token = request.session.get(OIDC_ACCESS_TOKEN_KEY)
        if request.META.get(OIDC_ACCESS_TOKEN_KEY):
            # request.META is assumed to have the latest access
            # token available, so refresh the one in the session
            # when it is available in request.META.
            access_token = request.META.get(OIDC_ACCESS_TOKEN_KEY)
            request.session.update({
                OIDC_ACCESS_TOKEN_KEY: access_token,
            })
        if not access_token:
            return self.logout_and_return_response(request)
        
        # Now that an access token has been found, verify that it can
        # still be used to query the UserInfo API. If it can't, perform
        # a logout.
        user_info = self.get_user_info(request, access_token)
        if not user_info:
            return self.logout_and_return_response(request)

        # The access token is still valid - so the login session can
        # be populated with relevant metadata.
        # "OIDC_CLAIM_sub" acts as the identifier for the current
        # session - it's better than other available identifiers.
        if request.META.get('OIDC_CLAIM_sub'):
            request.session.update({
                'user_id': request.META.get('OIDC_CLAIM_sub'),
            })
        self.copy_user_given_name_to_session(request, user_info)
        self.copy_user_privilege_info_to_session(request, user_info)

        try:
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
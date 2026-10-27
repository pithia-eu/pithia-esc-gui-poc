import logging
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from common.forms import InstitutionForLoginSessionForm
from user_management.services import (
    delete_institution_for_login_session,
    query_user_info_api,
    get_institution_id_for_login_session,
    get_institution_memberships_of_logged_in_user,
    get_subgroup_id_for_login_session,
    parse_eduperson_entitlement,
    set_institution_for_login_session,
)


logger = logging.getLogger(__name__)


class LoginMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Check that the access token is still valid. First, check that
        # there is an access token to check. If there isn't one, perform
        # a logout.
        # Latest (request.META), otherwise, use access token in session.
        access_token = self.get_latest_access_token(request)
        if not access_token:
            return self.logout_and_return_response(request)
        self.copy_access_token_to_session(request, access_token)
        
        # Now that an access token has been found, verify that it can
        # still be used to query the UserInfo API. If it can't, perform
        # a logout.
        user_info = self.get_user_info(request, access_token)
        if not user_info:
            messages.info(request, 'You have been logged out due to a period of inactivity.')
            return self.logout_and_return_response(request)

        # The access token is still valid - so the login session can
        # be populated with relevant metadata.
        self.copy_user_id_to_session(request)
        self.copy_user_given_name_to_session(request, user_info)
        self.copy_user_privilege_info_to_session(request, user_info)

        try:
            institution_id_logged_in_with = get_institution_id_for_login_session(request.session)
            if institution_id_logged_in_with is None:
                return self.get_response(request)

            memberships_of_logged_in_user = get_institution_memberships_of_logged_in_user(request.session)
            if memberships_of_logged_in_user is None:
                return self.get_response(request)

            # Check if still a member of the institution being used for the login
            # session. If not, invalidate the current login session's institution.
            is_user_still_member_of_institution_logged_in_with = (
                institution_id_logged_in_with in memberships_of_logged_in_user
            )
            if not is_user_still_member_of_institution_logged_in_with:
                delete_institution_for_login_session(request.session)
                return self.get_response(request)

            # User info is refreshed every request, so privileges stay up-to-date
            # and can be used to check and correct outdated privileges.
            is_user_authorisation_level_correct = get_subgroup_id_for_login_session(
                request.session
            ) == memberships_of_logged_in_user.get(institution_id_logged_in_with)

            if not is_user_authorisation_level_correct:
                # If authorisation level changed during the login
                # session, correct it here.
                set_institution_for_login_session(
                    request.session,
                    institution_id_logged_in_with,
                    memberships_of_logged_in_user.get(institution_id_logged_in_with)
                )
        except Exception:
            logger.exception(
                'Could not complete authentication due to an unexpected error. Resetting login session.'
            )
            return self.logout_and_return_response(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    ACCESS_TOKEN_SESSION_KEY = 'OIDC_access_token'
    def get_latest_access_token(self, request) -> str:
        return request.META.get(
            self.ACCESS_TOKEN_SESSION_KEY,
            request.session.get(self.ACCESS_TOKEN_SESSION_KEY)
        )

    def get_user_info(self, request, access_token: str):
        # Access token verification
        user_info = query_user_info_api(access_token)
        if 'error' in user_info:
            return None
        return user_info

    def copy_access_token_to_session(self, request, access_token: str):
        request.session.update({
            self.ACCESS_TOKEN_SESSION_KEY: access_token,
        })

    def copy_user_id_to_session(self, request):
        # "OIDC_CLAIM_sub" acts as the identifier for the current
        # session - it's better than other available identifiers,
        # like "OIDC_CLAIM_email", which isn't always guaranteed.
        request.session.update({
            'user_id': request.META.get('OIDC_CLAIM_sub'),
        })

    def copy_user_privilege_info_to_session(self, request, user_info: dict):
        request.session.update({
            'user_institution_subgroups': parse_eduperson_entitlement(
                user_info.get('eduperson_entitlement', [])
            )
        })

    def copy_user_given_name_to_session(self, request, user_info: dict):
        request.session.update({
            'user_given_name': user_info.get('given_name')
        })

    def logout_and_return_response(self, request):
        auth_logout(request)
        if '/authorised' not in request.path:
            # If not in a protected path, no need for further
            # login session management, just carry on with the
            # request.
            return self.get_response(request)
        return HttpResponseRedirect(reverse('home'))

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
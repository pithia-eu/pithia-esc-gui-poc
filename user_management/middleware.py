import logging
from django.http import HttpResponseRedirect
from django.contrib import messages
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
    remove_login_session_variables_and_redirect_user_to_logout_page,
    set_institution_for_login_session,
)


logger = logging.getLogger(__name__)


class LoginMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialisation.
        self.get_response = get_response

    def _verify_access_token_and_set_login_session_variables(self, request, access_token):
        # Access token verification
        user_info = get_user_info(access_token)
        if 'error' in user_info:
            # The User Info API will return an error if
            # the access token has been invalidated.
            raise Exception(f'An error was found in the user info response.')

            
        # Configuring login session variables
        # Store user info in session to minimise
        # calls to the User Info API.
        request.session['OIDC_access_token'] = access_token
        request.session['is_logged_in'] = True
        try:
            request.session['user_institution_subgroups'] = get_highest_subgroup_of_each_institution_for_logged_in_user(user_info['eduperson_entitlement'])
        except KeyError:
            request.session['user_institution_subgroups'] = {}
        request.session['user_id'] = request.META.get('OIDC_CLAIM_sub')
        request.session['user_given_name'] = user_info.get('given_name')

    def _update_session_access_token_if_possible(self, request):
        access_token_in_headers = request.META.get('OIDC_access_token')
        if not access_token_in_headers:
            return
        # Only update the session's access token if
        # there is one in the headers (setting it whilst
        # there isn't one may overwrite a valid access
        # token in the session).

        # Update the session's access token with every request
        # to ensure that any outdated session access tokens are
        # overwritten.
        request.session['OIDC_access_token'] = access_token_in_headers

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        try:
            # Verify if the user is logged in or not.
            # Check if an OIDC_access_token exists in
            # request.META, and perform the appropriate
            # action.
            self._update_session_access_token_if_possible(request)


            # The access token should always be retrieved from the
            # session. This is because the access token may not
            # always be present in the headers.
            access_token_in_session = request.session.get('OIDC_access_token')
            if not access_token_in_session:
                # Access token is not present, so assume that the
                # user is logged out.
                remove_login_session_variables(request.session)
                if '/authorised' in request.path:
                    return HttpResponseRedirect(reverse('home'))
            else:
                self._verify_access_token_and_set_login_session_variables(request, access_token_in_session)

            
            # Check if the user is still a member of the
            # institution they have logged in with. If not,
            # perform the appropriate action.
            logged_in_institution_id = get_institution_id_for_login_session(request.session)
            logged_in_institution_subgroup_id = get_subgroup_id_for_login_session(request.session)
            user_memberships = get_institution_memberships_of_logged_in_user(request.session)

            is_user_member_of_institution_for_login_session = (logged_in_institution_id is not None 
                                                                and user_memberships is not None
                                                                and logged_in_institution_id in user_memberships)
            # user_memberships gets updated with every request,
            # so it can be used to verify if a user's authorisation
            # level (decided by the highest level of subgroup they
            # are currently in), is still valid.
            is_user_authorisation_level_correct = (logged_in_institution_subgroup_id is not None
                                                    and user_memberships is not None
                                                    and logged_in_institution_subgroup_id == user_memberships.get(logged_in_institution_id))
            if (logged_in_institution_id is not None
                and not is_user_member_of_institution_for_login_session):
                delete_institution_for_login_session(request.session)
            elif (logged_in_institution_id is not None
                and not is_user_authorisation_level_correct):
                # If the user's permissions changed whilst
                # they are logged in, update the user's
                # permission level here.
                set_institution_for_login_session(
                    request.session,
                    logged_in_institution_id,
                    user_memberships.get(logged_in_institution_id)
                )
        except Exception:
            logger.exception('An unexpected error occurred during authentication.')
            messages.error('You have been logged out as there was a problem authenticating your login session. Please try logging in again.')
            return remove_login_session_variables_and_redirect_user_to_logout_page(request)

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
        except Exception:
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
            institution_selection_form = InstitutionForLoginSessionForm(
                institution_choices=institution_choices,
                initial={'next': request.path}
            )
            request.institution_selection_form = institution_selection_form
        except AttributeError:
            # session.get('user_memberships') will raise an AttributeError if
            # user memberships have not been stored in the session yet.
            pass
        except Exception:
            pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
from user_management.services import (
    get_user_info,
    get_highest_subgroup_of_each_institution_for_logged_in_user,
    remove_login_session_variables,
)

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
        if access_token is None:
            # If the access token is none, the
            # OIDC login session does not exist.
            remove_login_session_variables(request)
            return response
        
        if request.session['access_token'] == access_token:
            # If the session's access token is the same
            # as the one in request.META, there's shouldn't
            # be a need to set the login session variables
            # again.
            return response

        user_info = get_user_info(access_token)
        if 'error' not in user_info:
            # Store user info in session to minimise
            # calls to the UserInfo API.
            request.session['access_token'] = access_token
            request.session['is_logged_in'] = True
            request.session['user_institution_subgroups'] = get_highest_subgroup_of_each_institution_for_logged_in_user(user_info.get('eduperson_entitlement'))
            request.session['user_email'] = user_info.get('email')

        return response

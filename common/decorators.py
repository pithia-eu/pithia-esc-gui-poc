from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps

from user_management.services import get_institution_id_for_login_session

def login_session_institution_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        institution_id_for_login_session = get_institution_id_for_login_session(request)
        if not institution_id_for_login_session:
            messages.warning(request, 'The page cannot be accessed without setting an institution for this login session.')
            return HttpResponseRedirect(reverse('home'))
        return function(request, *args, **kwargs)

    return wrap
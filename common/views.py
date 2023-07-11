from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from functools import wraps

# Create your views here.
def institution_for_login_session_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if ((request.META.get('OIDC_access_token')
            or request.session.get('is_logged_in') is True)
            and reverse('choose_perun_organisation_subgroup_for_session') != request.path
            and reverse('logout') != request.path
            and 'institution_for_login_session' not in request.session
            and 'subgroup_for_login_session' not in request.session):
            return HttpResponseRedirect(reverse('choose_perun_organisation_subgroup_for_session'))
        return function(request, *args, **kwargs)
    
    return wrap

@method_decorator(institution_for_login_session_required, name='dispatch')
class LoginInstitutionRequiredView(TemplateView):
    pass
import environ
import os
import re
from django.http import (
    FileResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode

from help.services import (
    DataCollectionsHelpArticleContent,
    DataCollectionsSimpleSearchHelpArticleContent,
    SearchDataCollectionsByContentHelpArticleContent,
)
from pithiaesc.settings import BASE_DIR
from user_management.services import CREATION_URL_BASE

# Initialise environment variables
env = environ.Env()


from user_management.services import (
    CREATION_URL_BASE,
    remove_login_session_variables,
)

def logout(request):
    # Remove relevant session variables
    remove_login_session_variables(request.session)

    absolute_home_page_uri = re.sub(r'^http\b', 'https', request.build_absolute_uri(reverse("home")))
    return HttpResponseRedirect(f'/authorised/?{urlencode({"logout": absolute_home_page_uri})}')

def index(request):
    help_content_dicts = [
        DataCollectionsHelpArticleContent.as_dict(),
        DataCollectionsSimpleSearchHelpArticleContent.as_dict(),
        SearchDataCollectionsByContentHelpArticleContent.as_dict(),
    ]
    return render(request, 'index.html', {
        'title': 'PITHIA e-Science Centre',
        'create_institution_url': CREATION_URL_BASE,
        'help_content_dicts': help_content_dicts,
    })

def resource_registration_user_guide(request):
    try:
        return FileResponse(open(os.path.join(BASE_DIR, 'resource_management', 'PITHIA-NRF Data Registration User Guide.pdf'), 'rb'), content_type='application/pdf')
    except IOError:
        return HttpResponseNotFound('The data resource registration guide was not found.')
    
def terms_of_use(request):
    return render(request, 'terms-of-use.html', {
        'title': 'PITHIA e-Science Centre Acceptable Use Policy and Conditions of Use'
    })

def privacy_policy(request):
    return render(request, 'privacy-policy.html', {
        'title': 'PITHIA e-Science Centre Privacy Policy'
    })

def support(request):
    return render(request, 'support.html', {
        'title': 'Help & Support',
        'data_collections_help_article_title': DataCollectionsHelpArticleContent.title,
        'search_data_collections_by_content_help_article_title': SearchDataCollectionsByContentHelpArticleContent.title,
        'data_collection_simple_search_help_article_title': DataCollectionsSimpleSearchHelpArticleContent.title,
    })

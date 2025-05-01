import environ
import os
from django.http import (
    FileResponse,
    HttpResponseNotFound,
)
from django.shortcuts import (
    redirect,
    render,
)

from common.models import DataCollection
from help.services import (
    DataCollectionsHelpArticleContent,
    DataCollectionsSimpleSearchHelpArticleContent,
    SearchDataCollectionsByContentHelpArticleContent,
)
from ontology.services import (
    get_ontology_category_terms_in_xml_format,
    OntologyCategoryMetadataService,
)
from pithiaesc.settings import BASE_DIR
from user_management.services import CREATION_URL_BASE

# Initialise environment variables
env = environ.Env()


from user_management.services import (
    CREATION_URL_BASE,
    remove_login_session_variables_and_redirect_user_to_logout_page,
)

def logout(request):
    return remove_login_session_variables_and_redirect_user_to_logout_page(request)

def index(request):
    help_content_dicts = [
        DataCollectionsHelpArticleContent.as_dict(),
        DataCollectionsSimpleSearchHelpArticleContent.as_dict(),
        SearchDataCollectionsByContentHelpArticleContent.as_dict(),
    ]
    xml_of_features_of_interest = get_ontology_category_terms_in_xml_format('featureOfInterest')
    features_of_interest = OntologyCategoryMetadataService(xml_of_features_of_interest)
    data_collection_counts_by_fois = features_of_interest.get_first_two_layers_of_ontology_category()
    for foi_url in data_collection_counts_by_fois.keys():
        num_data_collections_using_foi = DataCollection.objects.referencing_feature_of_interest_urls([foi_url]).count()
        data_collection_counts_by_fois[foi_url].update({
            'count': num_data_collections_using_foi,
        })
    return render(request, 'index.html', {
        'title': 'PITHIA e-Science Centre',
        'create_institution_url': CREATION_URL_BASE,
        'help_content_dicts': help_content_dicts,
        'data_collection_counts_by_fois': data_collection_counts_by_fois,
    })

def data_provider_home(request):
    return redirect('home')

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

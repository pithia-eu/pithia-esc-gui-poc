from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .services import get_registered_features_of_interest


from common.constants import FEATURE_OF_INTEREST_URL_BASE
from common.models import StaticDatasetEntry
from search.views import BaseFeatureOfInterestSearchByContentTemplateView


_INDEX_PAGE_TITLE = 'Search Static Dataset Entries by Content'


# Create your views here.

class FeatureOfInterestSearchByContentTemplateView(BaseFeatureOfInterestSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return get_registered_features_of_interest()


def index(request):
    if request.method == 'POST':
        features_of_interests = request.POST.getlist('featureOfInterest')
        request.session['sde_features_of_interest'] = features_of_interests
        return HttpResponseRedirect(reverse('static_dataset_search:results'))
    return render(request, 'static_dataset_search/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'feature_of_interest_form_url': reverse('static_dataset_search:foi_form_template'),
    })


def results(request):
    feature_of_interest_urls = [
        f'{FEATURE_OF_INTEREST_URL_BASE}/{feature_of_interest_localid}'
        for feature_of_interest_localid in request.session.get('sde_features_of_interest', [])
    ]
    results = StaticDatasetEntry.objects.for_search(feature_of_interest_urls)

    # Display parameters user inputted in case they want to refine for the next search.
    parameters = dict()
    if len(request.session.get('sde_features_of_interest', [])):
        parameters.update({
            'Features of Interest': [
                f'{FEATURE_OF_INTEREST_URL_BASE}/{local_id}'
                for local_id in request.session.get('sde_features_of_interest', [])
            ],
        })

    return render(request, 'static_dataset_search/results.html', {
        'title': 'Static Dataset Search by Content Results',
        'parameters': parameters,
        'results': results,
        'search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })
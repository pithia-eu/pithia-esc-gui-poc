import os
from django.http import (
    FileResponse,
    Http404,
    HttpResponseServerError,
    HttpResponseNotFound,
)
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from .services import (
    create_dictionary_from_pithia_ontology_component,
    get_ontology_category_terms_in_xml_format,
)
from .utils import (
    LicenceOntologyTermMetadata,
    ObservedPropertyOntologyTermMetadata,
    OntologyCategoryMetadata,
    OntologyTermMetadata,
)

from common.models import (
    Organisation,
    Individual,
    Project,
    Platform,
    Operation,
    Instrument,
    AcquisitionCapabilities,
    Acquisition,
    ComputationCapabilities,
    Computation,
    Process,
    DataCollection,
    StaticDatasetEntry,
    DataSubset,
    Workflow,
    ScientificMetadata,
)
from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE
from pithiaesc.settings import BASE_DIR
from search.services import get_parents_of_registered_ontology_terms
from utils.string_helpers import split_camel_case


_ONTOLOGY_INDEX_PAGE_TITLE = 'Space Physics Ontology Browser'


# Create your views here.
def ontology(request):
    return render(request, 'ontology/index.html', {
        'title': _ONTOLOGY_INDEX_PAGE_TITLE
    })

def ontology_guide(request):
    try:
        return FileResponse(open(os.path.join(BASE_DIR, 'ontology', 'PITHIA-NRF_SpacePhysicsOntology_1.4.pdf'), 'rb'), content_type='application/pdf')
    except IOError:
        return HttpResponseNotFound('The ontology guide was not found.')
    
def _get_ontology_category_term_list_page_title_from_category(category):
    title_base = ' '.join(split_camel_case(category)).title()
    if category.lower() == 'crs':
        title_base = 'Co-ordinate Reference System'
    elif category.lower() == 'verticalcrs':
        title_base = 'Vertical Co-ordinate Reference System'
    return f'{title_base} Terms'

def ontology_category_terms_list(request, category):
    xml_for_ontology_category = get_ontology_category_terms_in_xml_format(category)
    ontology_category_metadata = OntologyCategoryMetadata(xml_for_ontology_category)
    return render(request, 'ontology/ontology_category_terms_list.html', {
        'category_list_url': reverse('ontology:ontology_category_terms_list_only', kwargs={'category': category}),
        'category': category,
        'category_description': ontology_category_metadata.description,
        'number_of_terms': ontology_category_metadata.number_of_terms,
        'title': _get_ontology_category_term_list_page_title_from_category(category),
        'ontology_index_page_breadcrumb_text': _ONTOLOGY_INDEX_PAGE_TITLE,
    })

def ontology_category_terms_list_only(request, category):
    try:
        dictionary = create_dictionary_from_pithia_ontology_component(category)
    except FileNotFoundError:
        return HttpResponseServerError('Could not load terms due to a server error.')
    registered_ontology_terms = list()
    parents_of_registered_ontology_terms = list()
    registered_ontology_server_urls = set()
    registrations = ScientificMetadata.objects.all()
    for r in registrations:
        for ontology_url in r.properties.ontology_urls:
            if ontology_url in registered_ontology_server_urls:
                continue
            if f'/{category}/'.lower() not in ontology_url.lower():
                continue
            registered_ontology_server_urls.add(ontology_url)
    registered_ontology_terms = [url.split('/')[-1] for url in list(registered_ontology_server_urls)]
    parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, [])
    return render(request, 'ontology/ontology_tree_template_outer.html', {
        'dictionary': dictionary,
        'category': category,
        'registered_ontology_terms': registered_ontology_terms,
        'parents_of_registered_ontology_terms': parents_of_registered_ontology_terms,
    })
 
class OntologyTermDetailView(TemplateView):
    template_name = 'ontology/detail/bases/base.html'

    def apply_wrapper_to_ontology_term_metadata(self, xml_string_for_ontology_term: str):
        return OntologyTermMetadata(xml_string_for_ontology_term)

    def get_registrations_referencing_ontology_term(self):
        ontology_iri = self.ontology_term_metadata.iri
        all_registrations_unsubclassed = ScientificMetadata.objects.all()
        registrations_referencing_ontology_term = {
            Organisation.type_plural_readable: list(),
            Individual.type_plural_readable: list(),
            Project.type_plural_readable: list(),
            Platform.type_plural_readable: list(),
            Operation.type_plural_readable: list(),
            Instrument.type_plural_readable: list(),
            AcquisitionCapabilities.type_plural_readable: list(),
            Acquisition.type_plural_readable: list(),
            ComputationCapabilities.type_plural_readable: list(),
            Computation.type_plural_readable: list(),
            Process.type_plural_readable: list(),
            DataCollection.type_plural_readable: list(),
            StaticDatasetEntry.type_plural_readable: list(),
            DataSubset.type_plural_readable: list(),
            Workflow.type_plural_readable: list(),
        }

        self.number_of_registrations_referencing_ontology_term = 0
        for r in all_registrations_unsubclassed:
            if not ontology_iri in r.properties.ontology_urls:
                continue
            r_subclassed = r.get_subclass_instance()
            if not r_subclassed:
                continue
            registrations_referencing_ontology_term[r_subclassed.type_plural_readable].append(r_subclassed)
            self.number_of_registrations_referencing_ontology_term += 1
        return registrations_referencing_ontology_term

    def get(self, request, *args, **kwargs):
        if not hasattr(self, 'category'):
            self.category = self.kwargs['category']
        self.term_id = self.kwargs['term_id']
        xml_string_for_ontology_category_terms = get_ontology_category_terms_in_xml_format(self.category)
        self.ontology_category_metadata = OntologyCategoryMetadata(xml_string_for_ontology_category_terms)
        xml_string_for_ontology_term = self.ontology_category_metadata.get_term_with_id(self.term_id)
        if not xml_string_for_ontology_term:
            raise Http404(f'An ontology term with ID, <b>"{self.term_id}"</b>, was not found.')
        self.ontology_term_metadata = self.apply_wrapper_to_ontology_term_metadata(xml_string_for_ontology_term)
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.ontology_term_metadata.pref_label,
            'resource_ontology_url': f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/{self.category}/{self.term_id}',
            'ontology_term_metadata': self.ontology_term_metadata,
            # Get names and ontology browser URLs for
            # ontology server URLs.
            'names_and_ontology_browser_urls': self.ontology_term_metadata.get_names_and_ontology_browser_urls_of_ontology_term_urls(
                fetched_ontology_categories={
                    self.category: self.ontology_category_metadata,
                }
            ),
            'category': self.category,
            'registrations_referencing_ontology_term': self.get_registrations_referencing_ontology_term(),
            'ontology_index_page_breadcrumb_text': _ONTOLOGY_INDEX_PAGE_TITLE,
            'ontology_category_term_list_page_breadcrumb_text': _get_ontology_category_term_list_page_title_from_category(self.category),
            'number_of_registrations_referencing_ontology_term': self.number_of_registrations_referencing_ontology_term,
        })
        return context


class LicenceTermDetailView(OntologyTermDetailView):
    template_name = 'ontology/detail/bases/licence.html'

    def apply_wrapper_to_ontology_term_metadata(self, xml_string_for_ontology_term: str):
        return LicenceOntologyTermMetadata(xml_string_for_ontology_term)

    def get(self, request, *args, **kwargs):
        self.category = 'licence'
        return super().get(request, *args, **kwargs)


class ObservedPropertyTermDetailView(OntologyTermDetailView):
    template_name = 'ontology/detail/bases/observed_property.html'

    def apply_wrapper_to_ontology_term_metadata(self, xml_string_for_ontology_term: str):
        return ObservedPropertyOntologyTermMetadata(xml_string_for_ontology_term)

    def get(self, request, *args, **kwargs):
        self.category = 'observedProperty'
        return super().get(request, *args, **kwargs)
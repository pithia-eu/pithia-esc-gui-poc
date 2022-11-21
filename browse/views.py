import re
from dateutil.parser import parse
from django.urls import reverse
from rdflib import URIRef
from rdflib.resource import Resource
from rdflib.namespace import _SKOS
from common import mongodb_models
from django.shortcuts import render
from bson.objectid import ObjectId
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView

from utils.url_helpers import create_ontology_term_detail_url_from_ontology_term_server_url
from utils.html_helpers import create_anchor_tag_html_from_ontology_term_details
from utils.ontology_helpers import create_dictionary_from_pithia_ontology_component, get_graph_of_pithia_ontology_component, ONTOLOGY_SERVER_BASE_URL
from validation.url_validation import PITHIA_METADATA_SERVER_HTTPS_URL_BASE, SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE
from search.helpers import remove_underscore_from_id_attribute
from search.views import get_parents_of_registered_ontology_terms, get_registered_computation_types, get_registered_features_of_interest, get_registered_instrument_types, get_registered_measurands, get_registered_observed_properties, get_registered_phenomenons

_RESOURCES_PAGE_TITLE = 'Browse Metadata'
_ONTOLOGY_PAGE_TITLE = 'Space Physics Ontology'
_XML_SCHEMAS_PAGE_TITLE = 'Metadata Models'

# Create your views here.
def index(request):
    return render(request, 'browse/index.html', {
        'title': 'Browse',
        'resources_page_title': _RESOURCES_PAGE_TITLE,
        'xml_schemas_page_title': _XML_SCHEMAS_PAGE_TITLE,
        'ontology_page_title': _ONTOLOGY_PAGE_TITLE,
    })

def resources(request):
    num_current_organsations = mongodb_models.CurrentOrganisation.count_documents({})
    num_current_individuals = mongodb_models.CurrentIndividual.count_documents({})
    num_current_projects = mongodb_models.CurrentProject.count_documents({})
    num_current_platforms = mongodb_models.CurrentPlatform.count_documents({})
    num_current_instruments = mongodb_models.CurrentInstrument.count_documents({})
    num_current_operations = mongodb_models.CurrentOperation.count_documents({})
    num_current_acquisition_capabilities = mongodb_models.CurrentAcquisitionCapability.count_documents({})
    num_current_acquisitions = mongodb_models.CurrentAcquisition.count_documents({})
    num_current_computation_capabilities = mongodb_models.CurrentComputationCapability.count_documents({})
    num_current_computations = mongodb_models.CurrentComputation.count_documents({})
    num_current_processes = mongodb_models.CurrentProcess.count_documents({})
    num_current_data_collections = mongodb_models.CurrentDataCollection.count_documents({})
    return render(request, 'browse/resources.html', {
        'title': _RESOURCES_PAGE_TITLE,
        'num_current_organisations': num_current_organsations,
        'num_current_individuals': num_current_individuals,
        'num_current_projects': num_current_projects,
        'num_current_platforms': num_current_platforms,
        'num_current_instruments': num_current_instruments,
        'num_current_operations': num_current_operations,
        'num_current_acquisition_capabilities': num_current_acquisition_capabilities,
        'num_current_acquisitions': num_current_acquisitions,
        'num_current_computation_capabilities': num_current_computation_capabilities,
        'num_current_computations': num_current_computations,
        'num_current_processes': num_current_processes,
        'num_current_data_collections': num_current_data_collections,
    })

def schemas(request):
    return render(request, 'browse/schemas.html', {
        'title': _XML_SCHEMAS_PAGE_TITLE
    })

def ontology(request):
    return render(request, 'browse/ontology.html', {
        'title': _ONTOLOGY_PAGE_TITLE
    })

# Credit for _split_camel_case() function: https://stackoverflow.com/a/37697078
def _split_camel_case(string):
    return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', string)).split()

def ontology_category_terms_list(request, category):
    title = ' '.join(_split_camel_case(category)).title()
    if category.lower() == 'crs':
        title = 'Co-ordinate Reference System'
    elif category.lower() == 'verticalcrs':
        title = 'Vertical Co-ordinate Reference System'
    title += ' Terms'
    return render(request, 'browse/ontology_category_terms_list.html', {
        'category': category,
        'title': title,
        'ontology_page_title': _ONTOLOGY_PAGE_TITLE,
    })

def ontology_category_terms_list_only(request, category):
    dictionary = create_dictionary_from_pithia_ontology_component(category)
    registered_ontology_terms = []
    parents_of_registered_ontology_terms = []
    if category.lower() == 'observedproperty':
        registered_ontology_terms = get_registered_observed_properties()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'featureofinterest':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_features_of_interest(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'instrumenttype':
        registered_ontology_terms = get_registered_instrument_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'computationtype':
        registered_ontology_terms = get_registered_computation_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'phenomenon':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_phenomenons(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'measurand':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_measurands(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    return render(request, 'browse/ontology_tree_template_outer.html', {
        'dictionary': dictionary,
        'category': category,
        'registered_ontology_terms': registered_ontology_terms,
        'parents_of_registered_ontology_terms': parents_of_registered_ontology_terms,
    })

def _remove_namespace_prefix_from_predicate(p):
    p_identifier_no_prefix = p.identifier.split('#')[-1]
    if len(p.identifier.split('#')) == 1:
        p_identifier_no_prefix = p.identifier.split('/')[-1]
    return p_identifier_no_prefix

def ontology_term_detail(request, category, term_id):
    g = get_graph_of_pithia_ontology_component(category)
    SKOS = _SKOS.SKOS
    resource = None
    resource_uriref = URIRef(f'{ONTOLOGY_SERVER_BASE_URL}{category}/{term_id}')
    triples = list(g.triples((None, SKOS.member, resource_uriref)))
    if len(triples) > 0:
        resource = Resource(g, triples[0][2])
    if resource is None:
        return HttpResponseNotFound(f'Details for the ontology term ID <b>"{term_id}"</b> were not found.')
    resource_predicates_no_prefix = list(set(map(_remove_namespace_prefix_from_predicate, resource.predicates())))
    # Turn resource into a dictionary for easier usage
    resource_dictionary = {}
    resource_predicates_readable = {}
    for p in resource.predicates():
        p_identifier_no_prefix = p.identifier.split('#')[-1]
        if len(p.identifier.split('#')) == 1:
            p_identifier_no_prefix = p.identifier.split('/')[-1]
        if p_identifier_no_prefix not in resource_dictionary and (p_identifier_no_prefix == 'observedProperty' or p_identifier_no_prefix == 'phenomenon' or p_identifier_no_prefix == 'measurand' or p_identifier_no_prefix == 'featureOfInterest' or p_identifier_no_prefix == 'propagationMode' or p_identifier_no_prefix == 'interaction' or p_identifier_no_prefix == 'qualifier' or p_identifier_no_prefix == 'narrower' or p_identifier_no_prefix == 'broader'):
            # Other ontology terms referenced by the resource
            if p_identifier_no_prefix == 'narrower' or p_identifier_no_prefix == 'broader':
                g_other_ontology_term = g
            else:
                g_other_ontology_term = get_graph_of_pithia_ontology_component(p_identifier_no_prefix)
            urls_of_referenced_terms = []
            urls_of_referenced_terms_with_preflabels = []
            for s2, p2, o2 in g.triples((resource_uriref, p.identifier, None)):
                urls_of_referenced_terms.append(str(o2))
            for u in urls_of_referenced_terms:
                ontology_term_detail_url_for_referenced_term = create_ontology_term_detail_url_from_ontology_term_server_url(u)
                term_pref_label = u.split('/')[-1]
                anchor_tag_of_term = create_anchor_tag_html_from_ontology_term_details(term_pref_label, u, ontology_term_detail_url_for_referenced_term, g_other_ontology_term)
                urls_of_referenced_terms_with_preflabels.append(anchor_tag_of_term)
            resource_dictionary[p_identifier_no_prefix]= urls_of_referenced_terms_with_preflabels
        if p_identifier_no_prefix not in resource_dictionary:
            if len(list(g.triples((resource_uriref, p.identifier, None)))) > 1:
                resource_dictionary[p_identifier_no_prefix] = []
                for s2, p2, o2 in g.triples((resource_uriref, p.identifier, None)):
                    resource_dictionary[p_identifier_no_prefix].append(str(o2))
            else:
                resource_dictionary[p_identifier_no_prefix] = str(list(g.triples((resource_uriref, p.identifier, None)))[0][2])
    # Have a human-readable version of the predicates to display in the front-end.
    for p in resource_predicates_no_prefix:
        if p == 'broader':
            resource_predicates_readable[p] = 'Broader Terms' 
        elif p == 'narrower':
            resource_predicates_readable[p] = 'Narrower Terms' 
        elif p == 'observedProperty':
            resource_predicates_readable[p] = 'Observed Properties' 
        elif p == 'phenomenon':
            resource_predicates_readable[p] = 'Phenomenons' 
        elif p == 'measurand':
            resource_predicates_readable[p] = 'Measurands' 
        elif p == 'featureOfInterest':
            resource_predicates_readable[p] = 'Features of Interest' 
        elif p == 'interaction':
            resource_predicates_readable[p] = 'Interactions' 
        elif p == 'qualifier':
            resource_predicates_readable[p] = 'Qualifiers'
        else:
            resource_predicates_readable[p] = ' '.join(_split_camel_case(p)).title() 
        category_readable = ' '.join(_split_camel_case(category)).title()
        if category.lower() == 'crs':
            category_readable = 'Co-ordinate Reference System'
        elif category.lower() == 'verticalcrs':
            category_readable = 'Vertical Co-ordinate Reference System'
    return render(request, 'browse/ontology_term_detail.html', {
        'title': resource_dictionary['prefLabel'],
        'ontology_page_title': _ONTOLOGY_PAGE_TITLE,
        'resource_ontology_url': f'{ONTOLOGY_SERVER_BASE_URL}{category}/{term_id}',
        'resource_dictionary': resource_dictionary,
        'resource_predicates_no_prefix': resource_predicates_no_prefix,
        'resource_predicates_readable': resource_predicates_readable,
        'category': category,
        'category_readable': category_readable,
    })

class ListResourcesView(TemplateView):
    template_name = 'browse/list_resources_of_type.html'
    description = ''
    resource_mongodb_model = None
    resource_type_plural = _RESOURCES_PAGE_TITLE
    resource_detail_view_name = ''
    resources_list = []

    def get_resources_list(self):
        resources_list = list(self.resource_mongodb_model.find({}))
        return list(map(remove_underscore_from_id_attribute, resources_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.resource_type_plural
        context['description'] = self.description
        context['list_resources_page_title'] = _RESOURCES_PAGE_TITLE
        context['breadcrumb_item_list_resources_of_type_text'] = self.resource_type_plural
        context['resource_type_plural'] = self.resource_type_plural
        context['resource_detail_view_name'] = self.resource_detail_view_name
        context['resources_list'] = self.get_resources_list()

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class list_organisations(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    resource_type_plural = 'Organisations'
    resource_detail_view_name = 'browse:organisation_detail'
    description = 'Data Provider/Owner organisation'

class list_individuals(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentIndividual
    resource_type_plural = 'Individuals'
    resource_detail_view_name = 'browse:individual_detail'
    description = 'An individual, acting in a particular role and associated with an Organisation'

class list_projects(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentProject
    resource_type_plural = 'Projects'
    resource_detail_view_name = 'browse:project_detail'
    description = 'An identifiable activity designed to accomplish a set of objectives'

class list_platforms(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentPlatform
    resource_type_plural = 'Platforms'
    resource_detail_view_name = 'browse:platform_detail'
    description = 'An identifiable object that brings the acquisition instrument(s) to the appropriate environment (e.g., satellite, ground observatory)'

class list_instruments(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentInstrument
    resource_type_plural = 'Instruments'
    resource_detail_view_name = 'browse:instrument_detail'
    description = 'An object responsible for interacting with the Feature of Interest in order to acquire Observed Property values'

class list_operations(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentOperation
    resource_type_plural = 'Operations'
    resource_detail_view_name = 'browse:operation_detail'
    description = 'Description of how a platform operates in order to support data acquisition by the instrument'

class list_acquisition_capabilities(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    resource_type_plural = 'Acquisition Capabilities'
    resource_detail_view_name = 'browse:acquisition_capability_detail'
    description = ''

class list_acquisitions(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    resource_type_plural = 'Acquisitions'
    resource_detail_view_name = 'browse:acquisition_detail'
    description = 'Interaction of the Instrument with the Feature of Interest to obtain its Observed Properties'

class list_computation_capabilities(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    resource_type_plural = 'Computation Capabilities'
    resource_detail_view_name = 'browse:computation_capability_detail'
    description = ''

class list_computations(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentComputation
    resource_type_plural = 'Computations'
    resource_detail_view_name = 'browse:computation_detail'
    description = 'Numerical calculation without interacting with the Feature of Interest; characterised by its numerical input and output'

class list_processes(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentProcess
    resource_type_plural = 'Processes'
    resource_detail_view_name = 'browse:process_detail'
    description = 'A designated procedure used to assign a number, term, or other symbols to a Phenomenon generating the Result; consists of Acquisitions and Computations'

class list_data_collections(ListResourcesView):
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    resource_type_plural = 'Data Collections'
    resource_detail_view_name = 'browse:data_collection_detail'
    description = 'Top-level definition of a collection of the model or measurement data, with CollectionResults pointing to its URL(s) for accessing the data. Note: data collections do not include begin and end times, please see Catalogue'

def flatten(d):
    out = {}
    if d is None:
        return out
    for key, value in d.items():
        if isinstance(value, dict):
            value = [value]
        if isinstance(value, list):
            index = 0
            for subdict in value:
                index = int(index) + 1
                deeper = flatten(subdict).items()
                out.update({
                    key + ' <b>' + str(index) + '</b>.' + key2: value2 for key2, value2 in deeper
                })
        else:
            out[key] = value
    return out

def _get_ontology_server_urls_from_flattened_resource(resource_flattened):
    ontology_server_urls = set()
    resource_server_urls = set()
    for key, value in resource_flattened.items():
        if key.endswith('@xlink:href') and value.startswith(SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE):
            ontology_server_urls.add(value)
        if key.endswith('@xlink:href') and value.startswith(PITHIA_METADATA_SERVER_HTTPS_URL_BASE):
            resource_server_urls.add(value)

    return list(ontology_server_urls), list(resource_server_urls)

def _update_flattened_resource_keys_to_human_readable_html(resource_flattened):
    hidden_keys = [
        '_id',
        'description',
    ]
    hidden_key_regex = [
        re.compile(r'^name'),
        re.compile(r'^contactinfo'),
        re.compile(r'^identifier'),
        re.compile(r'.*onlineresource <b>1</b>\.description'),
        re.compile(r'.*onlineresource <b>1</b>\.linkage'),
        # re.compile(r'.*onlineresource <b>1</b>\.name'),
    ]
    resource_human_readable = {}
    for key in resource_flattened:
        if key.startswith('@') or any(x == key.lower() for x in hidden_keys) or any(regex for regex in hidden_key_regex if re.match(regex, key.lower())):
            continue
        key_split_by_dot = key.split('.')
        human_readable_key_strings = []
        for string in key_split_by_dot:
            # If there is only one occurrence of a property
            # doesn't make sense to keep the number suffix
            is_only_numbered_key = True
            if string.endswith('<b>1</b>'):
                for key2 in resource_flattened:
                    if string.replace('<b>1</b>', '<b>2</b>') in key2:
                        is_only_numbered_key = False
            if is_only_numbered_key:
                string = string.replace('<b>1</b>', '')

            # Skip these strings
            if  string.startswith('#') or string == '@xlink:href':
                continue

            # Only keep the part of the key after the ':'
            if ':' in string:
                index_of_colon = string.index(':')
                string = string[index_of_colon + 1:]
            # Only keep the part of the key after the '@'
            if '@' in string:
                index_of_at_symbol = string.index('@')
                string = string[index_of_at_symbol + 1:]

            # Append the string that the be part of the 
            # human-readable key
            if string == '_id' or string.isupper():
                human_readable_key_strings.append(string)
            elif '_' in string:
                human_readable_string = ' '.join(string.split('_'))
                human_readable_string = ' '.join(_split_camel_case(human_readable_string))
                human_readable_key_strings.append(human_readable_string)
            else:
                human_readable_string = ' '.join(_split_camel_case(string))
                if not human_readable_string[0].isupper():
                    human_readable_string = human_readable_string.title()
                human_readable_key_strings.append(human_readable_string)
        human_readable_key_strings[-1] = f'<b>{human_readable_key_strings[-1]}</b>'
        human_readable_key_last_string = human_readable_key_strings[-1]
        human_readable_key_strings.pop()

        human_readable_key = ' > '.join(human_readable_key_strings).strip()
        if human_readable_key.startswith('Om:'):
            human_readable_key = human_readable_key.replace('Om:', '')
        if len(human_readable_key_strings):
            human_readable_key = f'{human_readable_key_last_string} <small class="text-muted fst-italic">(from {human_readable_key})</small>'
        else:
            human_readable_key = human_readable_key_last_string
        if human_readable_key != '':
            resource_human_readable[human_readable_key] = resource_flattened[key]
    return resource_human_readable

class ResourceDetailView(TemplateView):
    title = 'Resource Detail'
    resource = None
    resource_id = ''
    resource_mongodb_model = None
    resource_type_plural = _RESOURCES_PAGE_TITLE
    resource_flattened = None
    resource_human_readable = {}
    ontology_server_urls = []
    resource_server_urls = []
    list_resources_of_type_view_name = ''
    template_name = 'browse/detail.html'

    def get(self, request, *args, **kwargs):
        self.resource_human_readable = {}
        if self.resource is None:
            # Extra check done for data_collection() view
            self.resource = self.resource_mongodb_model.find_one({
                '_id': ObjectId(self.resource_id)
            })
        if self.resource is None:
            return HttpResponseNotFound('Resource not found.')
        self.resource_flattened = flatten(self.resource)
        self.ontology_server_urls, self.resource_server_urls = _get_ontology_server_urls_from_flattened_resource(self.resource_flattened)
        self.resource_human_readable = _update_flattened_resource_keys_to_human_readable_html(self.resource_flattened)
        self.title = self.resource['identifier']['PITHIA_Identifier']['localID']
        if 'name' in self.resource:
            self.title = self.resource['name']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['list_resources_page_title'] = _RESOURCES_PAGE_TITLE
        context['breadcrumb_item_list_resources_of_type_text'] = f'{self.resource_type_plural}'
        context['resource'] = self.resource
        context['resource_flattened'] = self.resource_flattened
        context['ontology_server_urls'] = self.ontology_server_urls
        context['resource_server_urls'] = self.resource_server_urls
        context['resource_human_readable'] = self.resource_human_readable
        context['resource_creation_date'] = parse(self.resource['identifier']['PITHIA_Identifier']['creationDate'])
        context['resource_last_modification_date'] = parse(self.resource['identifier']['PITHIA_Identifier']['lastModificationDate'])
        context['list_resources_of_type_view_name'] = self.list_resources_of_type_view_name
        context['server_url_conversion_url'] = reverse('utils:convert_server_urls')
        return context

class organisation_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    resource_type_plural = 'Organisations'
    list_resources_of_type_view_name = 'browse:list_organisations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().get(request, *args, **kwargs)

class individual_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentIndividual
    resource_type_plural = 'Individuals'
    list_resources_of_type_view_name = 'browse:list_individuals'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().get(request, *args, **kwargs)

class project_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentProject
    resource_type_plural = 'Projects'
    list_resources_of_type_view_name = 'browse:list_projects'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().get(request, *args, **kwargs)

class platform_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentPlatform
    resource_type_plural = 'Platforms'
    list_resources_of_type_view_name = 'browse:list_platforms'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().get(request, *args, **kwargs)

class instrument_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentInstrument
    resource_type_plural = 'Instruments'
    list_resources_of_type_view_name = 'browse:list_instruments'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().get(request, *args, **kwargs)

class operation_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentOperation
    resource_type_plural = 'Operations'
    list_resources_of_type_view_name = 'browse:list_operations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().get(request, *args, **kwargs)

class acquisition_capability_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    resource_type_plural = 'Acquisition Capabilities'
    list_resources_of_type_view_name = 'browse:list_acquisition_capabilities'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_id']
        return super().get(request, *args, **kwargs)

class acquisition_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    resource_type_plural = 'Acquisitions'
    list_resources_of_type_view_name = 'browse:list_acquisitions'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().get(request, *args, **kwargs)

class computation_capability_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    resource_type_plural = 'Computation Capabilities'
    list_resources_of_type_view_name = 'browse:list_computation_capabilities'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_id']
        return super().get(request, *args, **kwargs)

class computation_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentComputation
    resource_type_plural = 'Computations'
    list_resources_of_type_view_name = 'browse:list_computations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().get(request, *args, **kwargs)

class process_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentProcess
    resource_type_plural = 'Processes'
    list_resources_of_type_view_name = 'browse:list_processes'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().get(request, *args, **kwargs)

class data_collection_detail(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    resource_type_plural = 'Data Collections'
    list_resources_of_type_view_name = 'browse:list_data_collections'
    template_name = 'browse/detail_interaction_methods.html'
    interaction_methods = []
    link_interaction_methods = []

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        self.resource = self.resource_mongodb_model.find_one({
            '_id': ObjectId(self.resource_id)
        })
        if self.resource is None:
            return HttpResponseNotFound('Resource not found.')
        self.interaction_methods = mongodb_models.CurrentDataCollectionInteractionMethod.find({
            'data_collection_localid': self.resource['identifier']['PITHIA_Identifier']['localID']
        })
        if 'collectionResults' in self.resource:
            if 'source' in self.resource['collectionResults']:
                self.link_interaction_methods = self.resource['collectionResults']['source']

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_methods'] = list(self.interaction_methods)
        context['link_interaction_methods'] = list(self.link_interaction_methods)
        context['data_collection_id'] = self.resource_id
        
        return context
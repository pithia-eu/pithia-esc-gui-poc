import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from lxml import etree
from urllib.parse import quote

from .constants import (
    PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
)
from .converted_xml_correction_functions import *
from .managers import *
from .querysets import *
from .xml_metadata_mapping_shortcuts import (
    AcquisitionCapabilitiesXmlMappingShortcuts,
    AcquisitionXmlMappingShortcuts,
    DataSubsetXmlMappingShortcuts,
    StaticDatasetEntryXmlMappingShortcuts,
    StaticDatasetXmlMappingShortcuts,
    ComputationCapabilitiesXmlMappingShortcuts,
    ComputationXmlMappingShortcuts,
    DataCollectionXmlMappingShortcuts,
    IndividualXmlMappingShortcuts,
    InstrumentXmlMappingShortcuts,
    OperationXmlMappingShortcuts,
    OrganisationXmlMappingShortcuts,
    PlatformXmlMappingShortcuts,
    ProcessXmlMappingShortcuts,
    ProjectXmlMappingShortcuts,
    WorkflowXmlMappingShortcuts,
)


logger = logging.getLogger(__name__)


# Create your models here.
class ScientificMetadata(models.Model):
    weight = 0

    ORGANISATION = 'organisation'
    INDIVIDUAL = 'individual'
    PROJECT = 'project'
    PLATFORM = 'platform'
    OPERATION = 'operation'
    INSTRUMENT = 'instrument'
    ACQUISITION_CAPABILITIES = 'acquisition_capabilities'
    ACQUISITION = 'acquisition'
    COMPUTATION_CAPABILITIES = 'computation_capabilities'
    COMPUTATION = 'computation'
    PROCESS = 'process'
    DATA_COLLECTION = 'data_collection'
    CATALOGUE = 'catalogue'
    CATALOGUE_ENTRY = 'catalogue_entry'
    CATALOGUE_DATA_SUBSET = 'catalogue_data_subset'
    WORKFLOW = 'workflow'
    TYPE_CHOICES = [
        (ORGANISATION, 'Organisation'),
        (INDIVIDUAL, 'Individual'),
        (PROJECT, 'Project'),
        (PLATFORM, 'Platform'),
        (OPERATION, 'Operation'),
        (INSTRUMENT, 'Instrument'),
        (ACQUISITION_CAPABILITIES, 'Acquisition Capabilities'),
        (ACQUISITION, 'Acquisition'),
        (COMPUTATION_CAPABILITIES, 'Computation Capabilities'),
        (COMPUTATION, 'Computation'),
        (PROCESS, 'Process'),
        (DATA_COLLECTION, 'Data Collection'),
        (CATALOGUE, 'Catalogue'),
        (CATALOGUE_ENTRY, 'Catalogue Entry'),
        (CATALOGUE_DATA_SUBSET, 'Catalogue Data Subset'),
        (WORKFLOW, 'Workflow'),
    ]
    id = models.CharField(
        max_length=200,
        primary_key=True,
        db_column='sm_id'
    )
    institution_id = models.CharField(
        max_length=200,
        db_column='inst_id'
    )
    owner_id = models.CharField(
        max_length=200,
        db_column='owner_id'
    )
    type = models.CharField(
        max_length=100,
        choices=TYPE_CHOICES,
        db_column='sm_type'
    )
    xml = models.TextField(db_column='sm_metadata_file')
    json = models.JSONField(db_column='sm_json_support')
    deactivated = models.BooleanField(default=False, db_column='sm_deactivated')
    created_at = models.DateTimeField(auto_now_add=True, db_column='sm_reg_date')
    updated_at = models.DateTimeField(auto_now=True, db_column='sm_upd_date')

    # JSON field properties
    @property
    def identifier(self):
        return self.json['identifier']

    @property
    def pithia_identifier(self):
        return self.identifier['PITHIA_Identifier']

    @property
    def namespace(self):
        return self.pithia_identifier['namespace']

    @property
    def localid(self):
        return self.pithia_identifier['localID']
    
    @property
    def name(self):
        return self.json['name']
    
    @property
    def description(self):
        try:
            return self.json['description']
        except Exception:
            return ''

    @property
    def creation_date_json(self):
        return self.pithia_identifier['creationDate']
    
    @property
    def last_modification_date_json(self):
        return self.pithia_identifier['lastModificationDate']

    # Helper properties
    @property
    def type_in_metadata_server_url(self):
        pass

    @property
    def localid_base(self):
        pass

    @property
    def _metadata_server_url_base(self):
        return PITHIA_METADATA_SERVER_HTTPS_URL_BASE

    @property
    def metadata_server_url(self):
        return quote(f'{self._metadata_server_url_base}/{self.type_in_metadata_server_url}/{self.namespace}/{self.localid}', safe='/:?=&')
    
    @property
    def converted_xml_correction_function(self):
        return None
    
    @property
    def _browse_detail_page_url_name(self):
        return None
    
    @property
    def root_element_name(self):
        return None

    def _get_immediate_metadata_dependents_and_update_checked_metadata(
            self,
            checked_metadata: set = set(),
            up_to_weight: int = -1) -> list:
        scientific_metadata_model_subclasses_sorted = sorted(
            list(ScientificMetadata.__subclasses__()),
            key=lambda subclass: subclass.weight
        )
        if up_to_weight != -1:
            up_to_weight += 1
        scientific_metadata_models_in_range = scientific_metadata_model_subclasses_sorted[
            self.weight:up_to_weight
        ]
        potential_dependents = []
        immediate_dependents = []
        for m in scientific_metadata_models_in_range:
            potential_dependents += list(m.objects.filter(xml__icontains=self.localid))
        for pd in potential_dependents:
            parsed_xml = etree.fromstring(pd.xml.encode('utf-8'))
            url_mentions = parsed_xml.xpath(f"//*[contains(@xlink:href, '{self.metadata_server_url}')]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
            if pd.localid == self.localid:
                continue
            if len(url_mentions) < 1:
                continue
            immediate_dependents.append(pd)
        checked_metadata.add(str(self.pk))
        return immediate_dependents

    def _get_dependents_of_immediate_metadata_dependents_and_update_checked_metadata(
            self,
            immediate_metadata_dependents: list,
            checked_metadata: set = set(),
            up_to_weight: int = -1) -> list:
        all_dependents_of_dependents = []
        for imd in immediate_metadata_dependents:
            if any(str(imd.pk) == md_pk for md_pk in checked_metadata):
                continue
            dependents_of_imd, updated_checked_metadata = imd.get_metadata_dependents_and_checked_metadata(
                checked_metadata=checked_metadata,
                up_to_weight=up_to_weight
            )
            all_dependents_of_dependents += dependents_of_imd

        return all_dependents_of_dependents

    def get_metadata_dependents_and_checked_metadata(
            self,
            checked_metadata: set = set(),
            up_to_weight: int = -1) -> list:
        # Get the immediate metadata dependents first
        immediate_metadata_dependents = self._get_immediate_metadata_dependents_and_update_checked_metadata(
            checked_metadata=checked_metadata,
            up_to_weight=up_to_weight
        )
        # Get all deeper dependents for immediate metadata dependents
        dependents_of_immediate_metadata_dependents = self._get_dependents_of_immediate_metadata_dependents_and_update_checked_metadata(
            immediate_metadata_dependents,
            checked_metadata=checked_metadata,
            up_to_weight=up_to_weight
        )
        # Combine the immediate dependents and deeper dependents
        all_metadata_dependents = list(immediate_metadata_dependents) + list(dependents_of_immediate_metadata_dependents)
        # Sort and make sure all found dependents are unique
        return sorted(
            list({
                str(md.pk): md
                for md in all_metadata_dependents
            }.values()),
            key=lambda md: md.weight
        ), checked_metadata
    
    @property
    def _immediate_metadata_dependents(self) -> list:
        return self._get_immediate_metadata_dependents_and_update_checked_metadata()

    def _dependents_of_immediate_metadata_dependents(self, immediate_metadata_dependents) -> list:
        return self._get_dependents_of_immediate_metadata_dependents_and_update_checked_metadata(
            immediate_metadata_dependents
        )

    @property
    def metadata_dependents(self) -> list:
        metadata_dependents, checked_metadata = self.get_metadata_dependents_and_checked_metadata(
            checked_metadata=set()
        )
        return metadata_dependents
    
    objects = ScientificMetadataManager.from_queryset(ScientificMetadataQuerySet)()
    organisations = OrganisationManager.from_queryset(OrganisationQuerySet)()
    individuals = IndividualManager.from_queryset(IndividualQuerySet)()
    projects = ProjectManager.from_queryset(ProjectQuerySet)()
    platforms = PlatformManager.from_queryset(PlatformQuerySet)()
    operations = OperationManager.from_queryset(OperationQuerySet)()
    instruments = InstrumentManager.from_queryset(InstrumentQuerySet)()
    acquisition_capability_sets = AcquisitionCapabilitiesManager.from_queryset(AcquisitionCapabilitiesQuerySet)()
    acquisitions = AcquisitionManager.from_queryset(AcquisitionQuerySet)()
    computation_capability_sets = ComputationCapabilitiesManager.from_queryset(ComputationCapabilitiesQuerySet)()
    computations = ComputationManager.from_queryset(ComputationQuerySet)()
    processes = ProcessManager.from_queryset(ProcessQuerySet)()
    data_collections = DataCollectionManager.from_queryset(DataCollectionQuerySet)()
    static_datasets = StaticDatasetManager.from_queryset(StaticDatasetQuerySet)()
    static_dataset_entries = StaticDatasetEntryManager.from_queryset(StaticDatasetEntryQuerySet)()
    data_subsets = DataSubsetManager.from_queryset(DataSubsetQuerySet)()
    workflows = WorkflowManager.from_queryset(WorkflowQuerySet)()

    def save(self, *args, **kwargs):
        if self.converted_xml_correction_function is not None:
            self.json = self.converted_xml_correction_function(self.json)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(f'{self._browse_detail_page_url_name}', args=[str(self.pk)])
    
    class Meta:
        db_table = 'scien_metadata'

class InteractionMethod(models.Model):
    # Primary key should be handled automatically in the future
    id = models.CharField(max_length=36, primary_key=True, db_column='intm_id')
    scientific_metadata = models.ForeignKey(
        'ScientificMetadata',
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to=Q(type=ScientificMetadata.DATA_COLLECTION) | Q(type=ScientificMetadata.WORKFLOW),
        db_column='sm_id'
    )
    # owner = models.ForeignKey(
    #   'Member',
    #   db_column='owner_id'
    # )
    owner = models.CharField(
        max_length=200,
        db_column='owner_id'
    )
    API = 'api'
    MICADO = 'micado'
    DOWNLOAD = 'download'
    TYPE_CHOICES = [
        (API, 'API'),
        # (MICADO, 'MiCADO'),
        # (DOWNLOAD, 'Download'),
    ]
    type = models.CharField(
        choices=TYPE_CHOICES,
        default=API,
        max_length=100,
        db_column='intm_type'
    )
    config = models.JSONField(db_column='intm_config')
    deactivated = models.BooleanField(default=False, db_column='intm_deactivated')
    created_at = models.DateTimeField(auto_now_add=True, db_column='intm_reg_date')
    updated_at = models.DateTimeField(auto_now=True, db_column='intm_upd_date')

    objects = InteractionMethodManager()
    api_interaction_methods = APIInteractionMethodManager()
    workflow_api_interaction_methods = WorkflowAPIInteractionMethodManager()
    
    class Meta:
        db_table = 'int_method'

class APIInteractionMethod(InteractionMethod):
    @property
    def specification_url(self):
        return self.config['specification_url']
    
    @property
    def description(self):
        return self.config['description']
    
    @specification_url.setter
    def specification_url(self, value):
        self.config['specification_url'] = value
    
    @description.setter
    def description(self, value):
        self.config['description'] = value

    objects = APIInteractionMethodManager()

    class Meta:
        proxy = True

class WorkflowAPIInteractionMethod(InteractionMethod):
    @property
    def specification_url(self):
        return self.config['specification_url']
    
    @property
    def description(self):
        return self.config['description']
    
    @specification_url.setter
    def specification_url(self, value):
        self.config['specification_url'] = value
    
    @description.setter
    def description(self, value):
        self.config['description'] = value

    objects = WorkflowAPIInteractionMethodManager()

    class Meta:
        proxy = True

class Institution(models.Model):
    institution_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HandleURLMapping(models.Model):
    id = models.CharField(max_length=100, db_column='doi_id', primary_key=True)
    handle_name = models.CharField(max_length=100, db_column='doi_name')
    url = models.URLField(db_column='doi_url')

    objects = HandleURLMappingQuerySet.as_manager()

    class Meta:
        db_table = 'doi'

# Proxy models
class Organisation(ScientificMetadata):
    type_in_metadata_server_url = 'organisation'
    localid_base = 'Organisation'
    weight = 0
    type_readable = 'organisation'
    type_plural_readable = 'organisations'
    type_description_readable = 'Data Provider/Owner organisation.'
    _browse_detail_page_url_name = 'browse:organisation_detail'
    root_element_name = 'Organisation'

    objects = OrganisationManager.from_queryset(OrganisationQuerySet)()

    @property
    def short_name(self):
        return self.json['shortName']

    @property
    def properties(self):
        return OrganisationXmlMappingShortcuts(self.xml)

    class Meta:
        proxy = True

class Individual(ScientificMetadata):
    type_in_metadata_server_url = 'individual'
    localid_base = 'Individual'
    weight = 1
    type_readable = 'individual'
    type_plural_readable = 'individuals'
    type_description_readable = 'An individual, acting in a particular role and associated with an Organisation.'
    _browse_detail_page_url_name = 'browse:individual_detail'
    root_element_name = 'Individual'

    @property
    def description(self):
        return ''
    
    @property
    def organisation_url(self):
        return self.json['organisation']['@xlink:href']

    @property
    def properties(self):
        return IndividualXmlMappingShortcuts(self.xml)

    objects = IndividualManager.from_queryset(IndividualQuerySet)()

    class Meta:
        proxy = True

class Project(ScientificMetadata):
    type_in_metadata_server_url = 'project'
    localid_base = 'Project'
    weight = 2
    type_readable = 'project'
    type_plural_readable = 'projects'
    type_description_readable = 'An identifiable activity designed to accomplish a set of objectives.'
    converted_xml_correction_function = correct_project_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:project_detail'
    root_element_name = 'Project'

    @property
    def abstract(self):
        return self.json['abstract']

    @property
    def properties(self):
        return ProjectXmlMappingShortcuts(self.xml)

    objects = ProjectManager.from_queryset(ProjectQuerySet)()

    class Meta:
        proxy = True

class Platform(ScientificMetadata):
    type_in_metadata_server_url = 'platform'
    localid_base = 'Platform'
    weight = 3
    type_readable = 'platform'
    type_plural_readable = 'platforms'
    type_description_readable = 'An identifiable object that brings the acquisition instrument(s) to the appropriate environment (e.g., satellite, ground observatory).'
    converted_xml_correction_function = correct_platform_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:platform_detail'
    root_element_name = 'Platform'

    @property
    def properties(self):
        return PlatformXmlMappingShortcuts(self.xml)

    objects = PlatformManager.from_queryset(PlatformQuerySet)()

    class Meta:
        proxy = True

class Operation(ScientificMetadata):
    type_in_metadata_server_url = 'operation'
    localid_base = 'Operation'
    weight = 4
    type_readable = 'operation'
    type_plural_readable = 'operations'
    type_description_readable = 'Description of how a platform operates in order to support data acquisition by the instrument.'
    converted_xml_correction_function = correct_operation_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:operation_detail'
    root_element_name = 'Operation'

    objects = OperationManager.from_queryset(OperationQuerySet)()

    @property
    def properties(self):
        return OperationXmlMappingShortcuts(self.xml)

    class Meta:
        proxy = True

class Instrument(ScientificMetadata):
    type_in_metadata_server_url = 'instrument'
    localid_base = 'Instrument'
    weight = 5
    type_readable = 'instrument'
    type_plural_readable = 'instruments'
    type_description_readable = 'An object responsible for interacting with the Feature of Interest in order to acquire Observed Property values.'
    converted_xml_correction_function = correct_instrument_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:instrument_detail'
    root_element_name = 'Instrument'

    @property
    def operational_modes(self):
        return [om['InstrumentOperationalMode'] for om in self.json.get('operationalMode', [])]

    @property
    def operational_mode_ids(self):
        return [om['InstrumentOperationalMode']['id'] for om in self.json.get('operationalMode', [])]

    @property
    def instrument_type_url(self):
        return self.json['type']['@xlink:href']
    
    def get_operational_mode_by_id(self, operational_mode_id):
        try:
            for operational_mode in self.json['operationalMode']:
                operational_mode = operational_mode['InstrumentOperationalMode']
                if operational_mode['id'] == operational_mode_id:
                    return operational_mode
        except KeyError:
            pass
        return None

    @property
    def properties(self):
        return InstrumentXmlMappingShortcuts(self.xml)

    objects = InstrumentManager.from_queryset(InstrumentQuerySet)()

    class Meta:
        proxy = True

class AcquisitionCapabilities(ScientificMetadata):
    type_in_metadata_server_url = 'acquisitionCapabilities'
    localid_base = 'AcquisitionCapabilities'
    weight = 6
    type_readable = 'acquisition capabilities'
    type_plural_readable = 'acquisition capabilities'
    type_description_readable = 'List of Process Capability descriptions for a particular Instrument in its particular mode of operation.'
    converted_xml_correction_function = correct_acquisition_capability_set_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:acquisition_capability_set_detail'
    root_element_name = 'AcquisitionCapabilities'

    @property
    def observed_property_urls(self):
        try:
            return [process_capability['observedProperty']['@xlink:href'] for process_capability in self.json['capabilities']['processCapability']]
        except KeyError:
            return []

    @property
    def properties(self):
        return AcquisitionCapabilitiesXmlMappingShortcuts(self.xml)

    objects = AcquisitionCapabilitiesManager.from_queryset(AcquisitionCapabilitiesQuerySet)()

    class Meta:
        proxy = True

class Acquisition(ScientificMetadata):
    type_in_metadata_server_url = 'acquisition'
    localid_base = 'Acquisition'
    weight = 7
    type_readable = 'acquisition'
    type_plural_readable = 'acquisitions'
    type_description_readable = 'Interaction of the Instrument with the Feature of Interest to obtain its Observed Properties.'
    converted_xml_correction_function = correct_acquisition_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:acquisition_detail'
    root_element_name = 'Acquisition'

    @property
    def properties(self):
        return AcquisitionXmlMappingShortcuts(self.xml)

    objects = AcquisitionManager.from_queryset(AcquisitionQuerySet)()

    class Meta:
        proxy = True

class ComputationCapabilities(ScientificMetadata):
    type_in_metadata_server_url = 'computationCapabilities'
    localid_base = 'ComputationCapabilities'
    weight = 8
    type_readable = 'computation capabilities'
    type_plural_readable = 'computation capabilities'
    type_description_readable = 'List of Process Capability descriptions for a particular Computation component.'
    converted_xml_correction_function = correct_computation_capability_set_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:computation_capability_set_detail'
    root_element_name = 'ComputationCapabilities'

    @property
    def computation_type_urls(self):
        try:
            return [type['@xlink:href'] for type in self.json['type']]
        except KeyError:
            return []

    @property
    def observed_property_urls(self):
        try:
            return [process_capability['observedProperty']['@xlink:href'] for process_capability in self.json['capabilities']['processCapability']]
        except KeyError:
            return []

    @property
    def properties(self):
        return ComputationCapabilitiesXmlMappingShortcuts(self.xml)

    objects = ComputationCapabilitiesManager.from_queryset(ComputationCapabilitiesQuerySet)()

    class Meta:
        proxy = True

class Computation(ScientificMetadata):
    type_in_metadata_server_url = 'computation'
    localid_base = 'Computation'
    weight = 9
    type_readable = 'computation'
    type_plural_readable = 'computations'
    type_description_readable = 'Numerical calculation without interacting with the Feature of Interest; characterised by its numerical input and output.'
    converted_xml_correction_function = correct_computation_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:computation_detail'
    root_element_name = 'Computation'

    @property
    def properties(self):
        return ComputationXmlMappingShortcuts(self.xml)

    objects = ComputationManager.from_queryset(ComputationQuerySet)()

    class Meta:
        proxy = True

class Process(ScientificMetadata):
    type_in_metadata_server_url = 'process'
    localid_base = 'CompositeProcess'
    weight = 10
    type_readable = 'process'
    type_plural_readable = 'processes'
    type_description_readable = 'A designated procedure used to assign a number, term, or other symbols to a Phenomenon generating the Result; consists of Acquisitions and Computations.'
    converted_xml_correction_function = correct_process_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:process_detail'
    root_element_name = 'CompositeProcess'

    @property
    def properties(self):
        return ProcessXmlMappingShortcuts(self.xml)

    objects = ProcessManager.from_queryset(ProcessQuerySet)()

    class Meta:
        proxy = True

class DataCollection(ScientificMetadata):
    type_in_metadata_server_url = 'collection'
    localid_base = 'DataCollection'
    weight = 11
    type_readable = 'data collection'
    type_plural_readable = 'data collections'
    type_description_readable = 'Top-level definition of a collection of the model or measurement data, with CollectionResults pointing to its URL(s) for accessing the data.'
    converted_xml_correction_function = correct_data_collection_xml_converted_to_dict
    _browse_detail_page_url_name = 'browse:data_collection_detail'
    root_element_name = 'DataCollection'

    @property
    def first_related_party_url(self):
        return self.json['relatedParty'][0]['ResponsiblePartyInfo']['party']['@xlink:href']

    @property
    def feature_of_interest_urls(self):
        try:
            return [nr['@xlink:href'] for nr in self.json['om:featureOfInterest']['FeatureOfInterest']['namedRegion']]
        except BaseException:
            pass
        return []

    @property
    def type_urls(self):
        try:
            return [type['@xlink:href'] for type in self.json['type']]
        except KeyError:
            pass
        return []

    @property
    def link_interaction_methods(self):
        try:
            return self.json['collectionResults']['source']
        except KeyError:
            pass
        return []

    @property
    def permission_urls(self):
        try:
            permission_urls = self.json['permission']
            if isinstance(permission_urls, list):
                return permission_urls
            return [permission_urls]
        except KeyError:
            pass
        return []

    @property
    def properties(self):
        return DataCollectionXmlMappingShortcuts(self.xml)

    objects = DataCollectionManager.from_queryset(DataCollectionQuerySet)()

    class Meta:
        proxy = True


class StaticDatasetTypeDescriptionMixin:
    type_description_readable = '''
        A listing of events or investigations assembled to
        aid users in locating data of interest. Each Entry
        in a Static Dataset has distinct begin and end times
        and a list of registered Data Subsets with optional
        DOIs to their persistent storage.'''


class StaticDataset(ScientificMetadata, StaticDatasetTypeDescriptionMixin):
    type_in_metadata_server_url = 'staticDataset'
    localid_base = 'StaticDataset'
    weight = 12
    type_readable = 'static dataset'
    type_plural_readable = 'static datasets'
    _browse_detail_page_url_name = 'browse:static_dataset_detail'
    root_element_name = 'StaticDataset'

    @property
    def entries(self):
        return StaticDatasetEntry.objects.referencing_static_dataset_id(self.localid)

    @property
    def metadata_server_url(self):
        return quote(f'{self._metadata_server_url_base}/{self.type_in_metadata_server_url}/{self.namespace}/{self.name}/{self.localid}', safe='/:?=&')

    @property
    def properties(self):
        return StaticDatasetXmlMappingShortcuts(self.xml)

    objects = StaticDatasetManager.from_queryset(StaticDatasetQuerySet)()

    class Meta:
        proxy = True

class StaticDatasetEntry(ScientificMetadata, StaticDatasetTypeDescriptionMixin):
    type_in_metadata_server_url = 'staticDataset'
    localid_base = 'StaticDatasetEntry'
    weight = 13
    type_readable = 'static dataset entry'
    type_plural_readable = 'static dataset entries'
    _browse_detail_page_url_name = 'browse:static_dataset_entry_detail'
    root_element_name = 'StaticDatasetEntry'

    @property
    def name(self):
        return self.json['entryName']

    @property
    def description(self):
        return self.json['entryDescription']
    
    @property
    def static_dataset_url(self):
        try:
            return self.json['staticDatasetIdentifier']['@xlink:href']
        except KeyError:
            return ''

    @property
    def catalogue(self):
        return StaticDataset.objects.get_by_metadata_server_url(self.static_dataset_url)

    @property
    def data_subsets(self):
        return DataSubset.objects.referencing_static_dataset_entry_id(self.localid)

    @property
    def metadata_server_url(self):
        try:
            return quote(f'{self._metadata_server_url_base}/{self.type_in_metadata_server_url}/{self.namespace}/{self.catalogue.name}/{self.localid}', safe='/:?=&')
        except StaticDataset.DoesNotExist:
            return quote(f'{self._metadata_server_url_base}/{self.type_in_metadata_server_url}/{self.namespace}/{self.localid}', safe='/:?=&')

    @property
    def properties(self):
        return StaticDatasetEntryXmlMappingShortcuts(self.xml)

    objects = StaticDatasetEntryManager.from_queryset(StaticDatasetEntryQuerySet)()

    class Meta:
        proxy = True

class DataSubset(ScientificMetadata, StaticDatasetTypeDescriptionMixin):
    type_in_metadata_server_url = 'staticDataset'
    localid_base = 'DataSubset'
    weight = 14
    type_readable = 'data subset'
    type_plural_readable = 'data subsets'
    _browse_detail_page_url_name = 'browse:data_subset_detail'
    root_element_name = 'DataSubset'

    @property
    def name(self):
        return self.json['dataSubsetName']

    @property
    def description(self):
        return self.json['dataSubsetDescription']
    
    @property
    def data_collection_url(self):
        return self.json['dataCollection']['@xlink:href']
    
    @property
    def static_dataset_entry_url(self):
        return self.json['entryIdentifier']['@xlink:href']
    
    @property
    def static_dataset_entry(self):
        return StaticDatasetEntry.objects.get_by_metadata_server_url(self.static_dataset_entry_url)

    @property
    def catalogue(self):
        return self.static_dataset_entry.catalogue

    @property
    def metadata_server_url(self):
        try:
            return quote(f'{self._metadata_server_url_base}/{self.type_in_metadata_server_url}/{self.namespace}/{self.catalogue.name}/{self.localid}', safe='/:?=&')
        except ObjectDoesNotExist:
            pass
        except AttributeError:
            pass
        return quote(f'{self._metadata_server_url_base}/{self.type_in_metadata_server_url}/{self.namespace}/{self.localid}', safe='/:?=&')

    @property
    def properties(self):
        return DataSubsetXmlMappingShortcuts(self.xml)

    objects = DataSubsetManager.from_queryset(DataSubsetQuerySet)()

    class Meta:
        proxy = True


class Workflow(ScientificMetadata):
    type_in_metadata_server_url = 'workflow'
    localid_base = 'Workflow'
    weight = 15
    type_readable = 'workflow'
    type_plural_readable = 'workflows'
    type_description_readable = '''A workflow is a combination of different interconnected data collections executed repeatedly in an 
orchestrated pattern to produce its output result. The pattern in its general form is a directed acyclic 
graph (DAG) and in its simplest form, a linear sequence of steps.'''
    _browse_detail_page_url_name = 'browse:workflow_detail'
    root_element_name = 'Workflow'

    @property
    def details_url(self):
        return self.json['workflowDetails']['@xlink:href']

    @property
    def data_collection_url(self):
        return self.json['dataCollection']['@xlink:href']

    @property
    def properties(self):
        return WorkflowXmlMappingShortcuts(self.xml)

    objects = WorkflowManager.from_queryset(WorkflowQuerySet)()

    class Meta:
        proxy = True
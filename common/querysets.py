from django.db import models
from django.db.models import Q
from operator import itemgetter

from .core import *

from utils.url_helpers import get_namespace_and_localid_from_resource_url

class MetadataQuerySet(models.QuerySet, AbstractMetadataDatabaseQueries):
    def _get_by_namespace_and_localid(self, namespace: str, localid: str):
        return self.get(json__identifier__PITHIA_Identifier__namespace=namespace, json__identifier__PITHIA_Identifier__localid=localid)

    def get_by_metadata_server_url(self, metadata_server_url: str):
        namespace, localid = itemgetter('namespace', 'localid')(get_namespace_and_localid_from_resource_url(metadata_server_url))
        return self._get_by_namespace_and_localid(namespace, localid)
    
    def get_by_metadata_server_urls(self, metadata_server_urls: list):
        query = Q()
        for url in metadata_server_urls:
            namespace, localid = itemgetter('namespace', 'localid')(get_namespace_and_localid_from_resource_url(url))
            query |= Q(json__identifier__PITHIA_Identifier__namespace=namespace, json__identifier__PITHIA_Identifier__localID=localid)
        return self.get_by_metadata_server_url(query)


class OrganisationQuerySet(MetadataQuerySet, AbstractOrganisationDatabaseQueries):
    pass

class IndividualQuerySet(MetadataQuerySet, AbstractIndividualDatabaseQueries):
    pass

class ProjectQuerySet(MetadataQuerySet, AbstractProjectDatabaseQueries):
    pass

class PlatformQuerySet(MetadataQuerySet, AbstractPlatformDatabaseQueries):
    pass

class OperationQuerySet(MetadataQuerySet, AbstractOperationDatabaseQueries):
    pass

class InstrumentQuerySet(MetadataQuerySet, AbstractInstrumentDatabaseQueries):
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        query = Q()
        for url in instrument_type_urls:
            query |= Q(**{'json__type__@xlink:href__contains': url})
        return self.filter(query)

    def for_search(self, instrument_type_urls: list):
        return self.referencing_instrument_type_urls(instrument_type_urls)

class AcquisitionCapabilitiesQuerySet(MetadataQuerySet, AbstractAcquisitionCapabilitiesDatabaseQueries):
    def referencing_instrument_urls(self, instrument_urls: list):
        query = Q()
        for url in instrument_urls:
            query |= Q(**{'json__instrumentModePair__InstrumentOperationalModePair__instrument__@xlink:href': url})
        return self.filter(query)

    def referencing_observed_property_urls(self, observed_property_urls: list):
        query = Q()
        for url in observed_property_urls:
            query |= Q(**{'json__capabilities__processCapability__contains': [{'observedProperty': {'@xlink:href': url}}]})
        return self.filter(query)

    def for_search(self, instrument_urls: list, observed_property_urls: list):
        return self.referencing_instrument_urls(instrument_urls) & self.referencing_observed_property_urls(observed_property_urls)

class AcquisitionQuerySet(MetadataQuerySet, AbstractAcquisitionDatabaseQueries):
    def referencing_acquisition_capability_set_urls(self, acquisition_capability_set_urls: list):
        query = Q()
        for url in acquisition_capability_set_urls:
            query |= Q(**{'json__capabilityLinks__capabilityLink__contains': [{'acquisitionCapabilities': {'@xlink:href': url}}]})
        return self.filter(query)

    def for_search(self, acquisition_capability_set_urls: list):
        return self.referencing_acquisition_capability_set_urls(acquisition_capability_set_urls)

class ComputationCapabilitiesQuerySet(MetadataQuerySet, AbstractComputationCapabilitiesDatabaseQueries):
    def referencing_computation_type_urls(self, computation_type_urls: list):
        query = Q()
        for url in computation_type_urls:
            query |= Q(**{'json__type__@xlink:href': url})
        return self.filter(query)

    def referencing_observed_property_urls(self, observed_property_urls: list):
        query = Q()
        for url in observed_property_urls:
            query |= Q(**{'json__capabilities__processCapability__contains': [{'observedProperty': {'@xlink:href': url}}]})
        return self.filter(query)
    
    def referencing_computation_capability_set_url(self, computation_capability_set_url: str):
        return self.filter(json__childComputation__contains={'@xlink:href': computation_capability_set_url})
    
    def _immediate_computation_capability_set_referers(self, computation_capability_set):
        return self.referencing_computation_capability_set_url(computation_capability_set.metadata_server_url)
    
    def all_computation_capability_set_referers(self, computation_capability_set, initial_referers_list=[]):
        all_referers = initial_referers_list
        immediate_referers = list(self._immediate_computation_capability_set_referers(computation_capability_set))
        for ir in immediate_referers:
            if not any(str(ir.pk) == str(r.pk) for r in all_referers):
                all_referers.append(ir)
                all_referers += self.all_computation_capability_set_referers(ir)
        return list({str(r.pk): r for r in all_referers}.values())
    
    def _immediate_child_computations(self, computation_capability_set):
        child_computation_urls = [child_computation['@xlink:href'] for child_computation in computation_capability_set.json['childComputation']]
        return self.get_by_metadata_server_urls(child_computation_urls)
    
    def all_child_computations(self, computation_capability_set, initial_child_computation_list=[]):
        all_child_computations = initial_child_computation_list
        immediate_child_computations = list(self._immediate_child_computations(computation_capability_set))
        for icc in immediate_child_computations:
            if not any(icc.pk == cc.pk for cc in all_child_computations):
                all_child_computations.append(icc)
                self.all_child_computations(icc, all_child_computations)
        return all_child_computations

    def for_search(self, computation_type_urls: list, observed_property_urls: list):
        return self.referencing_computation_type_urls(computation_type_urls) & self.referencing_observed_property_urls(observed_property_urls)

class ComputationQuerySet(MetadataQuerySet, AbstractComputationDatabaseQueries):
    def referencing_computation_capability_set_urls(self, computation_capability_set_urls: list):
        query = Q()
        for url in computation_capability_set_urls:
            query |= Q(**{'json__capabilityLinks__capabilityLink__contains': [{'computationCapabilities': {'@xlink:href': url}}]})
        return self.filter(query)

    def for_search(self, computation_capability_set_urls: list):
        return self.referencing_computation_capability_set_urls(computation_capability_set_urls)

class ProcessQuerySet(MetadataQuerySet, AbstractProcessDatabaseQueries):
    def referencing_acquisition_urls(self, acquisition_urls: list):
        query = Q()
        for url in acquisition_urls:
            query |= Q(**{'json__acquisitionComponent__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def referencing_computation_urls(self, computation_urls: list):
        query = Q()
        for url in computation_urls:
            query |= Q(**{'json__computationComponent__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def for_search(self, acquisition_urls: list, computation_urls: list):
        return self.referencing_acquisition_urls(acquisition_urls) | self.referencing_computation_urls(computation_urls)

class DataCollectionQuerySet(MetadataQuerySet, AbstractDataCollectionDatabaseQueries):
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        query = Q()
        for url in instrument_type_urls:
            query |= Q(**{'json__type__@xlink:href': url})
        return self.filter(query)

    def referencing_computation_type_urls(self, computation_type_urls: list):
        query = Q()
        for url in computation_type_urls:
            query |= Q(**{'json__type__@xlink:href': url})
        return self.filter(query)

    def referencing_process_urls(self, process_urls: list):
        query = Q()
        for url in process_urls:
            query |= Q(**{'json__om:procedure__@xlink:href': url})
        return self.filter(query)

    def referencing_feature_of_interest_urls(self, feature_of_interest_urls: list):
        query = Q()
        for url in feature_of_interest_urls:
            query |= Q(**{'json__om:featureOfInterest__FeatureOfInterest__namedRegion__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def for_search(
        self,
        process_urls: list,
        feature_of_interest_urls: list,
        instrument_type_urls: list,
        computation_type_urls: list
    ):
        return self.referencing_process_urls(process_urls) \
            | self.referencing_instrument_type_urls(instrument_type_urls) \
            | self.referencing_computation_type_urls(computation_type_urls) \
            | self.referencing_feature_of_interest_urls(feature_of_interest_urls)

class CatalogueQuerySet(MetadataQuerySet, AbstractCatalogueDatabaseQueries):
    pass

class CatalogueEntryQuerySet(MetadataQuerySet, AbstractCatalogueEntryDatabaseQueries):
    pass

class CatalogueDataSubsetQuerySet(MetadataQuerySet, AbstractCatalogueDataSubsetDatabaseQueries):
    pass
import os

from django.db import models
from django.db.models import Q
from operator import itemgetter

from .abstract_classes import *

from utils.url_helpers import (
    divide_resource_url_from_op_mode_id,
    get_namespace_and_localid_from_resource_url,
)

class ScientificMetadataQuerySet(models.QuerySet, AbstractMetadataDatabaseQueries):
    def get_by_namespace_and_localid(self, namespace: str, localid: str):
        return self.get(json__identifier__PITHIA_Identifier__namespace=namespace, json__identifier__PITHIA_Identifier__localID=localid)

    def get_by_metadata_server_url(self, metadata_server_url: str):
        try:
            localid = metadata_server_url.split('/')[-1]
        except Exception:
            raise self.model.DoesNotExist
        return self.get(pk=localid)
    
    def get_by_metadata_server_urls(self, metadata_server_urls: list):
        if not metadata_server_urls:
            return self.none()
        query = Q()
        for url in metadata_server_urls:
            namespace, localid = get_namespace_and_localid_from_resource_url(url)
            query |= Q(json__identifier__PITHIA_Identifier__namespace=namespace, json__identifier__PITHIA_Identifier__localID=localid)
        return self.filter(query)

    def delete_by_metadata_server_urls(self, metadata_server_urls: list):
        if not metadata_server_urls:
            return
        localids = [get_namespace_and_localid_from_resource_url(url)[1] for url in metadata_server_urls]
        registrations_for_deletion = list(self.filter(json__identifier__PITHIA_Identifier__localID__in=localids))
        for r in registrations_for_deletion:
            r.delete(using=os.environ['DJANGO_RW_DATABASE_NAME'])

    def owned_by_institution(self, institution_id: str):
        return self.filter(institution_id=institution_id)


class OrganisationQuerySet(ScientificMetadataQuerySet, AbstractOrganisationDatabaseQueries):
    def for_simple_search(self, query_sections: list):
        search_query = Q()
        for qs in query_sections:
            search_query &= Q(json__name__icontains=qs)
        return self.filter(search_query)

class IndividualQuerySet(ScientificMetadataQuerySet, AbstractIndividualDatabaseQueries):
    def referencing_organisation_url(self, organisation_url: str):
        return self.filter(**{'json__organisation__@xlink:href': organisation_url})

    def for_delete_chain(self, metadata_server_url: str):
        referencing_organisation_url = self.referencing_organisation_url(metadata_server_url)
        return referencing_organisation_url

class ProjectQuerySet(ScientificMetadataQuerySet, AbstractProjectDatabaseQueries):
    def referencing_party_url(self, party_url: str):
        return self.filter(**{'json__relatedParty__contains': [{'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}]})

    def for_delete_chain(self, metadata_server_url: str):
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        return referencing_party_url

    def for_simple_search(self, query_sections: list):
        search_query = Q()
        for qs in query_sections:
            search_query &= Q(json__name__icontains=qs)
        return self.filter(search_query)

class PlatformQuerySet(ScientificMetadataQuerySet, AbstractPlatformDatabaseQueries):
    def referencing_party_url(self, party_url: str):
        return self.filter(**{'json__relatedParty__contains': [{'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}]})
    
    def referencing_platform_url(self, platform_url: str):
        return self.filter(**{'json__childPlatform__contains': [{'@xlink:href': platform_url}]})

    def for_delete_chain(self, metadata_server_url: str):
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        referencing_other_platforms = self.referencing_platform_url(metadata_server_url)
        return referencing_party_url | referencing_other_platforms

class OperationQuerySet(ScientificMetadataQuerySet, AbstractOperationDatabaseQueries):
    def referencing_party_url(self, party_url: str):
        return self.filter(**{'json__relatedParty__contains': [{'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}]})
    
    def referencing_platform_url(self, platform_url: str):
        return self.filter(**{'json__platform__contains': [{'@xlink:href': platform_url}]})

    def for_delete_chain(self, metadata_server_url: str):
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        referencing_platform_url = self.referencing_platform_url(metadata_server_url)
        return referencing_party_url | referencing_platform_url

class InstrumentQuerySet(ScientificMetadataQuerySet, AbstractInstrumentDatabaseQueries):
    def distinct_instrument_type_urls(self):
        return self.values_list('json__type__@xlink:href', flat=True).distinct()

    def get_by_operational_mode_url(self, operational_mode_url: str):
        metadata_server_url, op_mode_id = itemgetter('resource_url', 'op_mode_id')(divide_resource_url_from_op_mode_id(operational_mode_url))
        namespace, localid = get_namespace_and_localid_from_resource_url(metadata_server_url)
        return self.get(
            json__identifier__PITHIA_Identifier__namespace=namespace,
            json__identifier__PITHIA_Identifier__localID=localid,
            json__operationalMode__contains=[{'InstrumentOperationalMode': {'id': op_mode_id}}]
        )
    
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        if not instrument_type_urls:
            return self.none()
        query = Q()
        for url in instrument_type_urls:
            query |= Q(**{'json__type__@xlink:href__contains': url})
        return self.filter(query)
    
    def referencing_party_url(self, party_url: str):
        return self.filter(**{'json__relatedParty__contains': [{'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}]})

    def for_search_by_instrument_type_urls(self, instrument_type_urls: list):
        return self.referencing_instrument_type_urls(instrument_type_urls)
    
    def for_search(self, instrument_type_urls: list):
        return self.referencing_instrument_type_urls(instrument_type_urls)

    def for_delete_chain(self, metadata_server_url: str):
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        return referencing_party_url

class AcquisitionCapabilitiesQuerySet(ScientificMetadataQuerySet, AbstractAcquisitionCapabilitiesDatabaseQueries):
    def referencing_instrument_url(self, instrument_url: str):
        return self.filter(**{'json__instrumentModePair__InstrumentOperationalModePair__instrument__@xlink:href': instrument_url})

    def referencing_instrument_urls(self, instrument_urls: list):
        if not instrument_urls:
            return self.none()
        query = Q()
        for url in instrument_urls:
            query |= Q(**{'json__instrumentModePair__InstrumentOperationalModePair__instrument__@xlink:href': url})
        return self.filter(query)

    def referencing_observed_property_urls(self, observed_property_urls: list):
        if not observed_property_urls:
            return self.none()
        query = Q()
        for url in observed_property_urls:
            query |= Q(**{'json__capabilities__processCapability__contains': [{'observedProperty': {'@xlink:href': url}}]})
        return self.filter(query)
    
    def referencing_operational_mode_urls(self, operational_mode_urls: list):
        if not operational_mode_urls:
            return self.none()
        query = Q()
        for url in operational_mode_urls:
            query |= Q(**{'json__instrumentModePair__InstrumentOperationalModePair__mode__@xlink:href': url})
        return self.filter(query)

    def for_search_by_instrument_type_urls(self, instrument_urls: list):
        return self.referencing_instrument_urls(instrument_urls)

    def for_search_by_observed_property_urls(self, observed_property_urls: list):
        return self.referencing_observed_property_urls(observed_property_urls)

    def for_search(self, instrument_urls: list, observed_property_urls: list):
        results_referencing_instrument_urls = self.referencing_instrument_urls(instrument_urls)
        results_referencing_observed_property_urls = self.referencing_observed_property_urls(observed_property_urls)
        
        # If none are found to be referencing Instrument
        # URLs, just return those that are referencing
        # Observed Property URLs.
        if not instrument_urls:
            return results_referencing_observed_property_urls
        
        # If none are found to be referencing Observed
        # Property URLs, just return those that are
        # referencing Instrument URLs.
        if not observed_property_urls:
            return results_referencing_instrument_urls

        return results_referencing_instrument_urls & results_referencing_observed_property_urls
    
    def for_delete_chain(self, metadata_server_url: str, operational_mode_urls: list = []):
        referencing_instrument_url = self.referencing_instrument_url(metadata_server_url)
        referencing_operational_mode_urls = self.referencing_operational_mode_urls(operational_mode_urls)
        return referencing_instrument_url | referencing_operational_mode_urls

class AcquisitionQuerySet(ScientificMetadataQuerySet, AbstractAcquisitionDatabaseQueries):
    def referencing_acquisition_capability_set_url(self, acquisition_capability_set_url: str):
        return self.filter(**{'json__capabilityLinks__capabilityLink__contains': [{'acquisitionCapabilities': {'@xlink:href': acquisition_capability_set_url}}]})

    def referencing_acquisition_capability_set_urls(self, acquisition_capability_set_urls: list):
        if not acquisition_capability_set_urls:
            return self.none()
        query = Q()
        for url in acquisition_capability_set_urls:
            query |= Q(**{'json__capabilityLinks__capabilityLink__contains': [{'acquisitionCapabilities': {'@xlink:href': url}}]})
        return self.filter(query)
    
    def referencing_instrument_url(self, instrument_url: str):
        return self.filter(**{'json__instrument__@xlink:href': instrument_url})

    def referencing_platform_url(self, platform_url: str):
        return self.filter(**{'json__capabilityLinks__capabilityLink__contains': [{'platform': {'@xlink:href': platform_url}}]})

    def for_search_by_instrument_type_urls(self, acquisition_capability_set_urls: list):
        return self.referencing_acquisition_capability_set_urls(acquisition_capability_set_urls)

    def for_search_by_observed_property_urls(self, acquisition_capability_set_urls: list):
        return self.referencing_acquisition_capability_set_urls(acquisition_capability_set_urls)

    def for_search(self, acquisition_capability_set_urls: list):
        return self.referencing_acquisition_capability_set_urls(acquisition_capability_set_urls)
    
    def for_delete_chain(self, metadata_server_url: str):
        referencing_instrument_url = self.referencing_instrument_url(metadata_server_url)
        referencing_acquisition_capability_set_url = self.referencing_acquisition_capability_set_url(metadata_server_url)
        referencing_platform_url = self.referencing_platform_url(metadata_server_url)
        return referencing_instrument_url | referencing_acquisition_capability_set_url | referencing_platform_url

class ComputationCapabilitiesQuerySet(ScientificMetadataQuerySet, AbstractComputationCapabilitiesDatabaseQueries):
    def referencing_computation_type_urls(self, computation_type_urls: list):
        if not computation_type_urls:
            return self.none()
        query = Q()
        for url in computation_type_urls:
            query |= Q(**{'json__type__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def referencing_observed_property_urls(self, observed_property_urls: list):
        if not observed_property_urls:
            return self.none()
        query = Q()
        for url in observed_property_urls:
            query |= Q(**{'json__capabilities__processCapability__contains': [{'observedProperty': {'@xlink:href': url}}]})
        return self.filter(query)
    
    def referencing_computation_capability_set_url(self, computation_capability_set_url: str):
        return self.filter(json__childComputation__contains=[{'@xlink:href': computation_capability_set_url}])
    
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

    def _merge_computation_capability_set_referers_for_search(self, computation_capability_sets: list):
        # Find the Computation Capabilities referencing to the found
        # registrations.
        related_computation_capability_sets = []
        for cc in computation_capability_sets:
            related_computation_capability_sets += self.all_computation_capability_set_referers(cc, initial_referers_list=[])
        
        # Merge all results into a list of primary keys
        merged_list = computation_capability_sets + related_computation_capability_sets
        merged_list = list(set(cc.pk for cc in merged_list))

        # Convert everything back to QuerySets
        return self.filter(pk__in=merged_list)

    def for_search_by_computation_type_urls(self, computation_type_urls: list):
        computation_capability_sets = self.referencing_computation_type_urls(computation_type_urls)
        return self._merge_computation_capability_set_referers_for_search(list(computation_capability_sets))

    def for_search_by_observed_property_urls(self, observed_property_urls: list):
        computation_capability_sets = self.referencing_observed_property_urls(observed_property_urls)
        return self._merge_computation_capability_set_referers_for_search(list(computation_capability_sets))

    def for_search(self, computation_type_urls: list, observed_property_urls: list):
        # Find Computation Capabilities registrations by Computation Types
        # and Observed Properties
        results_referencing_computation_type_urls = self.referencing_computation_type_urls(computation_type_urls)
        results_referencing_observed_property_urls = self.referencing_observed_property_urls(observed_property_urls)
        referencing_available_urls = []
        if computation_type_urls and observed_property_urls:
            referencing_available_urls = list(
                results_referencing_computation_type_urls \
                & results_referencing_observed_property_urls
            )
        elif computation_type_urls:
            referencing_available_urls = list(results_referencing_computation_type_urls)
        elif observed_property_urls:
            referencing_available_urls = list(results_referencing_observed_property_urls)

        # Find the Computation Capabilities referencing to the found
        # registrations.
        related_computation_capability_sets = []
        for cc in referencing_available_urls:
            related_computation_capability_sets += self.all_computation_capability_set_referers(cc, initial_referers_list=[])

        # Merge all results into a list of primary keys
        merged_list = referencing_available_urls + related_computation_capability_sets
        merged_list = list(set(cc.pk for cc in merged_list))

        # Convert everything back to QuerySets
        return self.filter(pk__in=merged_list)
    
    def for_delete_chain(self, metadata_server_url: str):
        referencing_computation_capability_set_url = self.referencing_computation_capability_set_url(metadata_server_url)
        return referencing_computation_capability_set_url

class ComputationQuerySet(ScientificMetadataQuerySet, AbstractComputationDatabaseQueries):
    def referencing_computation_capability_set_url(self, computation_capability_set_url: str):
        return self.filter(**{'json__capabilityLinks__capabilityLink__contains': [{'computationCapabilities': {'@xlink:href': computation_capability_set_url}}]})

    def referencing_computation_capability_set_urls(self, computation_capability_set_urls: list):
        if not computation_capability_set_urls:
            return self.none()
        query = Q()
        for url in computation_capability_set_urls:
            query |= Q(**{'json__capabilityLinks__capabilityLink__contains': [{'computationCapabilities': {'@xlink:href': url}}]})
        return self.filter(query)

    def for_search_by_computation_type_urls(self, computation_capability_set_urls: list):
        return self.referencing_computation_capability_set_urls(computation_capability_set_urls)

    def for_search_by_observed_property_urls(self, computation_capability_set_urls: list):
        return self.referencing_computation_capability_set_urls(computation_capability_set_urls)

    def for_search(self, computation_capability_set_urls: list):
        return self.referencing_computation_capability_set_urls(computation_capability_set_urls)
    
    def for_delete_chain(self, metadata_server_url: str):
        referencing_computation_capability_set_url = self.referencing_computation_capability_set_url(metadata_server_url)
        return referencing_computation_capability_set_url

class ProcessQuerySet(ScientificMetadataQuerySet, AbstractProcessDatabaseQueries):
    def referencing_acquisition_url(self, acquisition_url: str):
        return self.filter(**{'json__acquisitionComponent__contains': [{'@xlink:href': acquisition_url}]})

    def referencing_acquisition_urls(self, acquisition_urls: list):
        if not acquisition_urls:
            return self.none()
        query = Q()
        for url in acquisition_urls:
            query |= Q(**{'json__acquisitionComponent__contains': [{'@xlink:href': url}]})
        return self.filter(query)
    
    def referencing_computation_url(self, computation_url: str):
        return self.filter(**{'json__computationComponent__contains': [{'@xlink:href': computation_url}]})

    def referencing_computation_urls(self, computation_urls: list):
        if not computation_urls:
            return self.none()
        query = Q()
        for url in computation_urls:
            query |= Q(**{'json__computationComponent__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def for_search_by_instrument_type_urls(self, acquisition_urls: list):
        return self.referencing_acquisition_urls(acquisition_urls)

    def for_search_by_computation_type_urls(self, computation_urls: list):
        return self.referencing_computation_urls(computation_urls)

    def for_search_by_observed_property_urls(self, acquisition_urls: list, computation_urls: list):
        return self.referencing_acquisition_urls(acquisition_urls) \
            | self.referencing_computation_urls(computation_urls)

    def for_search(self, acquisition_urls: list, computation_urls: list):
        return self.referencing_acquisition_urls(acquisition_urls) \
            | self.referencing_computation_urls(computation_urls)
    
    def for_delete_chain(self, metadata_server_url: str):
        referencing_acquisition_url = self.referencing_acquisition_url(metadata_server_url)
        referencing_computation_url = self.referencing_computation_url(metadata_server_url)
        return referencing_acquisition_url | referencing_computation_url

class DataCollectionQuerySet(ScientificMetadataQuerySet, AbstractDataCollectionDatabaseQueries):
    def referencing_feature_of_interest_urls(self, feature_of_interest_urls: list):
        if not feature_of_interest_urls:
            return self.none()
        query = Q()
        for url in feature_of_interest_urls:
            query |= Q(**{'json__om:featureOfInterest__FeatureOfInterest__namedRegion__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def referencing_computation_type_urls(self, computation_type_urls: list):
        if not computation_type_urls:
            return self.none()
        query = Q()
        for url in computation_type_urls:
            query |= Q(**{'json__type__contains': [{'@xlink:href': url}]})
        return self.filter(query)
    
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        if not instrument_type_urls:
            return self.none()
        query = Q()
        for url in instrument_type_urls:
            query |= Q(**{'json__type__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def referencing_annotation_type_urls(self, annotation_type_urls: list):
        if not annotation_type_urls:
            return self.none()
        query = Q()
        for url in annotation_type_urls:
            query |= Q(**{'json__type__contains': [{'@xlink:href': url}]})
        return self.filter(query)
    
    def referencing_party_url(self, party_url: str):
        return self.filter(**{'json__relatedParty__contains': [{'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}]})
    
    def referencing_process_url(self, process_url: str):
        return self.filter(**{'json__om:procedure__@xlink:href': process_url})

    def referencing_process_urls(self, process_urls: list):
        if not process_urls:
            return self.none()
        query = Q()
        for url in process_urls:
            query |= Q(**{'json__om:procedure__@xlink:href': url})
        return self.filter(query)
    
    def referencing_project_url(self, project_url: list):
        return self.filter(**{'json__project__contains': [{'@xlink:href': project_url}]})

    def for_search_by_feature_of_interest_urls(self, feature_of_interest_urls: list):
        return self.referencing_feature_of_interest_urls(feature_of_interest_urls)

    def for_search_by_instrument_type_urls(self, instrument_type_urls: list, process_urls: list):
        return self.referencing_instrument_type_urls(instrument_type_urls) \
            | self.referencing_process_urls(process_urls)

    def for_search_by_computation_type_urls(self, computation_type_urls: list, process_urls: list):
        return self.referencing_computation_type_urls(computation_type_urls) \
            | self.referencing_process_urls(process_urls)

    def for_search_by_annotation_type_urls(self, annotation_type_urls: list):
        return self.referencing_annotation_type_urls(annotation_type_urls)

    def for_search_by_observed_property_urls(self, process_urls: list):
        return self.referencing_process_urls(process_urls)

    def for_final_search_step(
            self,
            data_collections_found_by_feature_of_interest,
            data_collections_found_by_instrument_type,
            data_collections_found_by_computation_type,
            data_collections_found_by_annotation_type,
            data_collections_found_by_observed_property):
        search_results = self.all()
        if data_collections_found_by_feature_of_interest:
            search_results &= data_collections_found_by_feature_of_interest
        if data_collections_found_by_instrument_type:
            search_results &= data_collections_found_by_instrument_type
        if data_collections_found_by_computation_type:
            search_results &= data_collections_found_by_computation_type
        if data_collections_found_by_annotation_type:
            search_results &= data_collections_found_by_annotation_type
        if data_collections_found_by_observed_property:
            search_results &= data_collections_found_by_observed_property
        return search_results

    def for_search(
        self,
        process_urls: list,
        feature_of_interest_urls: list,
        instrument_type_urls: list,
        computation_type_urls: list
    ):
        search_results = self.all()
        results_referencing_process_urls = self.referencing_process_urls(process_urls)
        results_referencing_instrument_type_urls = self.referencing_instrument_type_urls(instrument_type_urls)
        results_referencing_computation_type_urls = self.referencing_computation_type_urls(computation_type_urls)
        results_referencing_feature_of_interest_urls = self.referencing_feature_of_interest_urls(feature_of_interest_urls)

        if process_urls:
            search_results &= results_referencing_process_urls
        if instrument_type_urls:
            search_results &= results_referencing_instrument_type_urls
        if computation_type_urls:
            search_results &= results_referencing_computation_type_urls
        if feature_of_interest_urls:
            search_results &= results_referencing_feature_of_interest_urls

        return search_results

    def for_delete_chain(self, metadata_server_url: str):
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        referencing_project_url = self.referencing_project_url(metadata_server_url)
        referencing_process_url = self.referencing_process_url(metadata_server_url)
        return referencing_party_url | referencing_project_url | referencing_process_url

class StaticDatasetQuerySet(ScientificMetadataQuerySet, AbstractStaticDatasetDatabaseQueries):
    pass

class StaticDatasetEntryQuerySet(ScientificMetadataQuerySet, AbstractStaticDatasetEntryDatabaseQueries):
    def referencing_static_dataset_url(self, static_dataset_url: str):
        return self.filter(**{'json__staticDatasetIdentifier__@xlink:href': static_dataset_url})
    
    def referencing_static_dataset_id(self, static_dataset_id: str):
        return self.filter(**{'json__staticDatasetIdentifier__@xlink:href__endswith': static_dataset_id})

    def for_delete_chain(self, metadata_server_url: str):
        referencing_static_dataset_url = self.referencing_static_dataset_url(metadata_server_url)
        return referencing_static_dataset_url

class DataSubsetQuerySet(ScientificMetadataQuerySet, AbstractDataSubsetDatabaseQueries):
    def referencing_static_dataset_entry_url(self, static_dataset_entry_url: str):
        return self.filter(**{'json__entryIdentifier__@xlink:href': static_dataset_entry_url})

    def referencing_static_dataset_entry_id(self, static_dataset_entry_id: str):
        return self.filter(**{'json__entryIdentifier__@xlink:href__endswith': static_dataset_entry_id})

    def referencing_data_collection_url(self, data_collection_url: str):
        return self.filter(**{'json__dataCollection__@xlink:href': data_collection_url})

    def for_delete_chain(self, metadata_server_url: str):
        referencing_data_collection_url = self.referencing_data_collection_url(metadata_server_url)
        referencing_static_dataset_entry_url = self.referencing_static_dataset_entry_url(metadata_server_url)
        return referencing_data_collection_url | referencing_static_dataset_entry_url

class WorkflowQuerySet(ScientificMetadataQuerySet, AbstractWorkflowDatabaseQueries):
    pass
    
class HandleURLMappingQuerySet(AbstractHandleURLMappingDatabaseQueries, models.QuerySet):
    def for_url(self, url):
        return self.filter(url=url)
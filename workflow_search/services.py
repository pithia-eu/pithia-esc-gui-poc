import re

from common.constants import (
    ANNOTATION_TYPE_URL_BASE,
    COMPUTATION_TYPE_URL_BASE,
    INSTRUMENT_TYPE_URL_BASE,
)
from common.models import (
    Acquisition,
    AcquisitionCapabilities,
    Computation,
    ComputationCapabilities,
    DataCollection,
    Instrument,
    Process,
    Workflow,
)
from data_collection_search.services import get_data_collections_for_search
from ontology.services import ObservedPropertyMetadataService


class WorkflowSearchService:
    @classmethod
    def search(
            cls,
            feature_of_interest_urls: list[str],
            annotation_type_urls: list[str],
            computation_type_urls: list[str],
            instrument_type_urls: list[str],
            observed_property_urls: list[str]):
        data_collections = get_data_collections_for_search(
            feature_of_interest_urls=feature_of_interest_urls,
            annotation_type_urls=annotation_type_urls,
            computation_type_urls=computation_type_urls,
            instrument_type_urls=instrument_type_urls,
            observed_property_urls=observed_property_urls,
        )
        data_collection_urls = [
            data_collection.metadata_server_url
            for data_collection in data_collections
        ]
        return Workflow.objects.referencing_data_collection_urls(
            data_collection_urls
        )


class OntologyTermsRegisteredWithWorkflows:
    @classmethod
    def _get_workflow_data_collections(cls):
        workflows = Workflow.objects.all()
        workflow_data_collection_urls = [
            dc_url
            for w in workflows
            for dc_url in w.properties.data_collection_urls
        ]
        return DataCollection.objects.get_by_metadata_server_urls(
            workflow_data_collection_urls
        )

    @classmethod
    def _get_workflow_processes(cls):
        # Data Collections
        workflow_data_collections = cls._get_workflow_data_collections()
        # Processes
        process_urls = cls._get_metadata_urls_of_type_from_registrations(
            workflow_data_collections,
            'process_urls'
        )
        return Process.objects.get_by_metadata_server_urls(process_urls)

    @classmethod
    def _get_workflow_acquisition_capabilities(cls, processes: list = list()):
        # Processes
        if not processes:
            processes = cls._get_workflow_processes()
        # Acquisitions
        acquisition_urls = cls._get_metadata_urls_of_type_from_registrations(
            processes,
            'acquisition_urls'
        )
        acquisitions = Acquisition.objects.get_by_metadata_server_urls(acquisition_urls)
        # Acquisition Capabilities
        acquisition_capabilities_urls = cls._get_metadata_urls_of_type_from_registrations(
            acquisitions,
            'acquisition_capabilities_urls'
        )
        return AcquisitionCapabilities.objects.get_by_metadata_server_urls(
            acquisition_capabilities_urls
        )

    @classmethod
    def _get_workflow_computation_capabilities(cls, processes: list = list()):
        # Processes
        if not processes:
            processes = cls._get_workflow_processes()
        # Computations
        computation_urls = cls._get_metadata_urls_of_type_from_registrations(
            processes,
            'computation_urls'
        )
        computations = Computation.objects.get_by_metadata_server_urls(computation_urls)
        # Computation Capabilities
        computation_capabilities_urls = cls._get_metadata_urls_of_type_from_registrations(
            computations,
            'computation_capabilities_urls'
        )
        return ComputationCapabilities.objects.get_by_metadata_server_urls(
            computation_capabilities_urls
        )

    @classmethod
    def _get_metadata_urls_of_type_from_registrations(
            cls,
            registrations: list,
            properties_attribute_name: str):
        return [
            url
            for r in registrations
            for url in getattr(r.properties, properties_attribute_name)
        ]

    # Features of interest
    @classmethod
    def get_registered_features_of_interest(cls):
        foi_ids = [
            foi_url.split('/')[-1]
            for wf_dc in cls._get_workflow_data_collections()
            for foi_url in wf_dc.properties.features_of_interest
            if foi_url.split('/')[-1]
        ]
        return foi_ids

    # Annotation types
    @classmethod
    def _get_annotation_type_urls_from_workflow_data_collections(cls):
        # Annotation type URLs should only be used with data
        # collections.
        workflow_data_collections = cls._get_workflow_data_collections()
        return set(
            type_url
            for wf_dc in workflow_data_collections
            for type_url in wf_dc.properties.types
            if re.match(f'^{ANNOTATION_TYPE_URL_BASE}', type_url)
        )

    @classmethod
    def get_registered_annotation_types(cls):
        annotation_type_urls = cls._get_annotation_type_urls_from_workflow_data_collections()
        return list(set(
            annotation_type_url.split('/')[-1]
            for annotation_type_url in annotation_type_urls
            if annotation_type_url.split('/')[-1]
        ))

    # Computation types
    @classmethod
    def _get_computation_type_urls_from_workflow_data_collections(cls):
        computation_capability_sets = cls._get_workflow_computation_capabilities()
        return list(set(
            type_url
            for cc in computation_capability_sets
            for type_url in cc.properties.types
            if re.match(f'^{COMPUTATION_TYPE_URL_BASE}', type_url)
        ))

    @classmethod
    def get_registered_computation_types(cls):
        computation_type_urls = cls._get_computation_type_urls_from_workflow_data_collections()
        return list(set(
            computation_type_url.split('/')[-1]
            for computation_type_url in computation_type_urls
            if computation_type_url.split('/')[-1]
        ))

    # Instrument types
    @classmethod
    def _get_instrument_type_urls_from_workflow_data_collections(cls):
        acquisition_capability_sets = cls._get_workflow_acquisition_capabilities()
        # Instruments
        instrument_urls = cls._get_metadata_urls_of_type_from_registrations(
            acquisition_capability_sets,
            'instrument_urls'
        )
        instruments = Instrument.objects.get_by_metadata_server_urls(instrument_urls)
        return list(set(
            instrument.properties.type
            for instrument in instruments
            if re.match(f'^{INSTRUMENT_TYPE_URL_BASE}', instrument.properties.type)
        ))

    @classmethod
    def get_registered_instrument_types(cls):
        instrument_type_urls = cls._get_instrument_type_urls_from_workflow_data_collections()
        return list(set(
            instrument_type_url.split('/')[-1]
            for instrument_type_url in instrument_type_urls
            if instrument_type_url.split('/')[-1]
        ))

    # Observed properties
    @classmethod
    def _get_observed_property_urls_from_workflow_data_collections(cls):
        observed_property_urls = []
        # Processes
        workflow_processes = cls._get_workflow_processes()
        observed_property_urls += [
            observed_property_url
            for p in workflow_processes
            for observed_property_url in p.properties.observed_property_urls
        ]
        # Acquisition capabilities
        workflow_acquisition_capabilities = cls._get_workflow_acquisition_capabilities(
            processes=workflow_processes
        )
        observed_property_urls += [
            observed_property_url
            for ac in workflow_acquisition_capabilities
            for observed_property_url in ac.properties.observed_property_urls
        ]
        # Computation capabilities
        workflow_computation_capabilities = cls._get_workflow_computation_capabilities(
            processes=workflow_processes
        )
        observed_property_urls += [
            observed_property_url
            for cc in workflow_computation_capabilities
            for observed_property_url in cc.properties.observed_property_urls
        ]
        return set(observed_property_urls)

    @classmethod
    def get_registered_observed_properties(cls):
        observed_property_urls = cls._get_observed_property_urls_from_workflow_data_collections()
        return list(set(
            observed_property_url.split('/')[-1]
            for observed_property_url in observed_property_urls
            if observed_property_url.split('/')[-1]
        ))

    @classmethod
    def get_registered_measurands(cls):
        observed_property_urls = cls._get_observed_property_urls_from_workflow_data_collections()
        observed_property_ontology_category = ObservedPropertyMetadataService()
        measurand_urls = observed_property_ontology_category.get_measurands_from_observed_properties(
            observed_property_urls
        )
        return list(set(
            measurand_url.split('/')[-1]
            for measurand_url in measurand_urls
            if measurand_url.split('/')[-1]
        ))

    @classmethod
    def get_registered_phenomenons(cls):
        observed_property_urls = cls._get_observed_property_urls_from_workflow_data_collections()
        observed_property_ontology_category = ObservedPropertyMetadataService()
        phenomenon_urls = observed_property_ontology_category.get_phenomenons_from_observed_properties(
            observed_property_urls
        )
        return list(set(
            phenomenon_url.split('/')[-1]
            for phenomenon_url in phenomenon_urls
            if phenomenon_url.split('/')[-1]
        ))
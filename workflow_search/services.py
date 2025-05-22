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
        ))

    # Computation types
    @classmethod
    def _get_computation_type_urls_from_workflow_data_collections(cls):
        # Data collections
        workflow_data_collections = cls._get_workflow_data_collections()
        # Processes
        process_urls = cls._get_metadata_urls_of_type_from_registrations(
            workflow_data_collections,
            'process_urls'
        )
        processes = Process.objects.get_by_metadata_server_urls(process_urls)
        # Computations - get computation type URLs from computation
        # capabilities.
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
        computation_capability_sets = ComputationCapabilities.objects.get_by_metadata_server_urls(
            computation_capabilities_urls
        )
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
        ))

    # Instrument types
    @classmethod
    def _get_instrument_type_urls_from_workflow_data_collections(cls):
        # Data collections
        workflow_data_collections = cls._get_workflow_data_collections()
        # Processes
        process_urls = cls._get_metadata_urls_of_type_from_registrations(
            workflow_data_collections,
            'process_urls'
        )
        processes = Process.objects.get_by_metadata_server_urls(process_urls)
        # Acquisitions - get instrument type URLs from instruments.
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
        acquisition_capability_sets = AcquisitionCapabilities.objects.get_by_metadata_server_urls(
            acquisition_capabilities_urls
        )
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
        ))
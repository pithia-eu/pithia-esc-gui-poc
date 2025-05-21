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
            metadata_urls_attribute_name: str):
        return [
            url
            for r in registrations
            for url in getattr(r.properties, metadata_urls_attribute_name)
        ]

    @classmethod
    def _get_type_urls_from_workflow_data_collections(cls):
        type_urls = []
        # Data Collections
        workflow_data_collections = cls._get_workflow_data_collections()
        type_urls += [
            type_url
            for wf_dc in workflow_data_collections
            for type_url in wf_dc.properties.types
        ]
        # Processes
        process_urls = cls._get_metadata_urls_of_type_from_registrations(
            workflow_data_collections,
            'process_urls'
        )
        processes = Process.objects.get_by_metadata_server_urls(process_urls)
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
        computation_capability_sets = ComputationCapabilities.objects.get_by_metadata_server_urls(
            computation_capabilities_urls
        )
        type_urls += [
            type_url
            for cc in computation_capability_sets
            for type_url in cc.properties.types
        ]
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
        acquisition_capability_sets = AcquisitionCapabilities.objects.get_by_metadata_server_urls(
            acquisition_capabilities_urls
        )
        # Instruments
        instrument_urls = cls._get_metadata_urls_of_type_from_registrations(
            acquisition_capability_sets,
            'instrument_urls'
        )
        instruments = Instrument.objects.get_by_metadata_server_urls(instrument_urls)
        type_urls += [
            instrument.properties.type
            for instrument in instruments
        ]
        return list(set(type_urls))

    @classmethod
    def get_registered_features_of_interest(cls):
        foi_ids = [
            foi_url.split('/')[-1]
            for wf_dc in cls._get_workflow_data_collections()
            for foi_url in wf_dc.properties.features_of_interest
        ]
        return foi_ids

    @classmethod
    def get_registered_computation_types(cls):
        pass
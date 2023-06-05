from abc import (
    ABC,
    abstractmethod,
)

class AbstractMetadataDatabaseQueries(ABC):
    @abstractmethod
    def _get_by_namespace_and_localid(self, namespace: str, localid: str):
        """
        A metadata registration using the passed in
        namespace and localID.
        """
        pass
    
    @abstractmethod
    def get_by_metadata_server_url(self, metadata_server_url: str):
        """
        A metadata registration corresponding to the
        metadata server URL passed in.
        """
        pass

    @abstractmethod
    def get_by_metadata_server_urls(self, metadata_server_urls: list):
        """
        Metadata registrations corresponding to at least
        one of the URLs from a list of metadata server URLs.
        """
        pass

class AbstractOrganisationDatabaseQueries(ABC):
    pass

class AbstractIndividualDatabaseQueries(ABC):
    @abstractmethod
    def referencing_organisation_url(self, organisation_url: str):
        """
        Individuals referencing a given Organisation URL.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Individuals referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractProjectDatabaseQueries(ABC):
    @abstractmethod
    def referencing_party_url(self, party_url: str):
        """
        Projects referencing a given Organisation
        or Individual URL.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Projects referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractPlatformDatabaseQueries(ABC):
    @abstractmethod
    def referencing_party_url(self, party_url: str):
        """
        Platforms referencing a given Organisation
        or Individual URL.
        """
        pass

    @abstractmethod
    def referencing_platform_url(self, platform_url: str):
        """
        Platforms referencing a given Platform URL.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Platforms referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractOperationDatabaseQueries(ABC):
    @abstractmethod
    def referencing_party_url(self, party_url: str):
        """
        Operations referencing a given Organisation
        or Individual URL.
        """
        pass

    @abstractmethod
    def referencing_platform_url(self, platform_url: str):
        """
        Operations referencing a given Platform URL.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Operations referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractInstrumentDatabaseQueries(ABC):
    @abstractmethod
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        """
        Instruments referencing at least one URL from
        a list of Instrument Type URLs.
        """
        pass

    @abstractmethod
    def for_search(self, instrument_type_urls: list):
        """
        Instruments referencing at least one URL
        from a list of Instrument Type URLs.
        """
        pass
    
    @abstractmethod
    def referencing_party_url(self, party_url: str):
        """
        Instruments referencing a given Organisation
        or Individual URL.
        """
        pass
    
    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Instruments referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractAcquisitionCapabilitiesDatabaseQueries(ABC):
    @abstractmethod
    def referencing_instrument_url(self, instrument_url: str):
        """
        Acquisition Capabilities registrations referencing a given
        Instrument URL.
        """
        pass
    
    @abstractmethod
    def referencing_instrument_urls(self, instrument_urls: list):
        """
        Acquisition Capabilities referencing at least one URL from
        a list of Instrument URLs.
        """
        pass

    @abstractmethod
    def referencing_observed_property_urls(self, observed_property_urls: list):
        """
        Acquisition Capabilities referencing at least one URL from
        a list of Observed Property URLs.
        """
        pass

    @abstractmethod
    def referencing_operational_mode_urls(self, operational_mode_urls: list):
        """
        Acquisition Capabilities referencing at least one URL from
        a list of operational mode URLs.
        """
        pass

    @abstractmethod
    def for_search(self, instrument_urls: list, observed_property_urls: list):
        """
        Acquisition Capabilities matching both of the following criteria:
        * Referencing at least one URL from a list of
          Instrument URLs.
        * Referencing at least one URL from a list of
          Observed Property URLs.

        If one list is empty, only the non-empty list for its
        corresponding condition must be true.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str, operational_mode_urls: list = []):
        """
        Acquisition Capabilities referencing a URL
        corresponding to a metadata registration
        that is planned for deletion.
        """
        pass

class AbstractAcquisitionDatabaseQueries(ABC):
    @abstractmethod
    def referencing_acquisition_capability_set_url(self, acquisition_capability_set_url: str):
        """
        Acquisitions referencing a given Acquisition
        Capabilities URL.
        """
        pass

    @abstractmethod
    def referencing_acquisition_capability_set_urls(self, acquisition_capability_set_urls: list):
        """
        Acquisitions referencing at least one URL from
        a list of Acquisition Capabilities.
        """
        pass

    @abstractmethod
    def referencing_instrument_url(self, instrument_url: str):
        """
        Acquisitions referencing a given Instrument URL.
        """
        pass

    @abstractmethod
    def for_search(self, acquisition_capability_set_urls: list):
        """
        Acquisitions referencing at least one URL from a
        list of Acquisition Capabilities URLs.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Acquisitions referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractComputationCapabilitiesDatabaseQueries(ABC):
    @abstractmethod
    def referencing_computation_type_urls(self, computation_type_urls: list):
        """
        Computation Capabilities referencing at least one URL from a
        list of Computation Type URLs.
        """
        pass

    @abstractmethod
    def referencing_computation_capability_set_url(self, computation_capability_set_url: str):
        """
        Computation Capabilities referencing the passed in
        Computation Capabilities URL.
        """
        pass

    @abstractmethod
    def _immediate_computation_capability_set_referers(self, computation_capability_set):
        """
        Computation Capabilities registrations referencing a given
        Computation Capabilities registration.
        """
        pass

    @abstractmethod
    def all_computation_capability_set_referers(self, computation_capability_set, initial_referers_list=[]):
        """
        Computation Capabilities registrations referencing the passed
        in Computation Capabilities registration, in addition to
        recursively performing the same process on each referer.
        """
        pass

    @abstractmethod
    def _immediate_child_computations(self, computation_capability_set):
        """
        Child Computation Capabilities registrations of a given Computation Capabilities
        registration.
        """
        pass

    @abstractmethod
    def all_child_computations(self, computation_capability_set, initial_child_computation_list=[]):
        """
        Child computation Capabilities registrations referencing the passed
        in Computation Capabilities registration, in addition to
        recursively performing the same process on each child Computation
        Capabilities registration.
        """
        pass

    @abstractmethod
    def referencing_observed_property_urls(self, observed_property_urls: list):
        """
        Computation Capabilities referencing at least one URL from a
        list of Observed Property URLs.
        """
        pass

    @abstractmethod
    def for_search(self, computation_type_urls: list, observed_property_urls: list):
        """
        Computation Capabilities matching both of the following criteria:
        * Referencing at least one URL from a list
          of Computation Type URLs.
        * Referencing at least one URL from a list
          of Observed Property URLs.

        If one list is empty, only the non-empty list for its
        corresponding condition must be true.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Computation Capabilities referencing a URL
        corresponding to a metadata registration
        that is planned for deletion.
        """
        pass

class AbstractComputationDatabaseQueries(ABC):
    @abstractmethod
    def referencing_computation_capability_set_url(self, computation_capability_set_url: str):
        """
        Computations referencing a given Computation
        Capabilities URL.
        """
        pass

    @abstractmethod
    def referencing_computation_capability_set_urls(self, computation_capability_set_urls: list):
        """
        Computations referencing at least one URL from a list
        of Computation Capabilities by URL in the passed in list.
        """
        pass

    @abstractmethod
    def for_search(self, computation_capability_set_urls: list):
        """
        Computations referencing at least one URL from a list
        of Computation Capabilities URLs.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Computations referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractProcessDatabaseQueries(ABC):
    @abstractmethod
    def referencing_acquisition_url(self, acquisition_url: str):
        """
        Processes referencing a given Acquisition URL.
        """
        pass

    @abstractmethod
    def referencing_acquisition_urls(self, acquisition_urls: list):
        """
        Processes referencing at least one URL from a list
        of Acquisition URLs.
        """
        pass

    @abstractmethod
    def referencing_computation_url(self, computation_url: str):
        """
        Processes referencing a given Computation URL.
        """
        pass

    @abstractmethod
    def referencing_computation_urls(self, computation_urls: list):
        """
        Processes referencing at least one URL from a list
        of Computation URLs.
        """
        pass

    @abstractmethod
    def for_search(self, acquisition_urls: list, computation_urls: list):
        """
        Processes meeting at least one of the following criteria:
        * Referencing at least one URL from a list of Acquisition URLs
        * Referencing at least one URL from a list of Computation URLs
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Processes referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractDataCollectionDatabaseQueries(ABC):
    @abstractmethod
    def referencing_computation_type_urls(self, computation_type_urls: list):
        """
        Data Collections referencing at least one URL
        from a list of Computation Type URLs.
        """
        pass

    @abstractmethod
    def referencing_feature_of_interest_urls(self, feature_of_interest_urls: list):
        """
        Data Collections referencing at least one URL
        from a list of Feature of Interest URLs.
        """
        pass

    @abstractmethod
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        """
        Data Collections referencing at least one URL
        from a list of Instrument Type URLs.
        """
        pass

    @abstractmethod
    def referencing_party_url(self, party_url: str):
        """
        Data Collections referencing a given Organisation
        or Individual URL.
        """
        pass

    @abstractmethod
    def referencing_process_url(self, process_url: str):
        """
        Data Collections referencing a given Process URL.
        """
        pass

    @abstractmethod
    def referencing_process_urls(self, process_urls: list):
        """
        Data Collections referencing at least one URL
        from a list of Process URLs.
        """
        pass

    @abstractmethod
    def referencing_project_url(self, project_url: list):
        """
        Data Collections referencing a given Project URL.
        """
        pass

    @abstractmethod
    def for_search(
        self,
        process_urls: list,
        feature_of_interest_urls: list,
        instrument_type_urls: list,
        computation_type_urls: list
    ):
        """
        Data Collections meeting at least one of the following
        criteria:
        * Referencing at least one URL from a
          list of Process URLs
        * Referencing at least one URL from a
          list of Feature of Interest URLs
        * Referencing at least one URL from
          a list of Instrument Type URLs
        * Referencing at least one URL from a
          list of Computation Type URLs
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Data Collections referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        pass

class AbstractCatalogueDatabaseQueries(ABC):
    pass

class AbstractCatalogueEntryDatabaseQueries(ABC):
    @abstractmethod
    def referencing_catalogue_url(self, catalogue_url: str):
        """
        Catalogue Entries referencing a given Catalogue URL.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Catalogue Entries referencing a URL corresponding
        to a metadata registration that is planned for
        deletion.
        """
        pass

class AbstractCatalogueDataSubsetDatabaseQueries(ABC):
    @abstractmethod
    def referencing_catalogue_entry_url(self, catalogue_entry_url: str):
        """
        Catalogue Data Subsets referencing a given Catalogue
        Entry URL.
        """
        pass

    @abstractmethod
    def referencing_data_collection_url(self, data_collection_url: str):
        """
        Catalogue Data Subsets referencing a given Data
        Collection URL.
        """
        pass

    @abstractmethod
    def for_delete_chain(self, metadata_server_url: str):
        """
        Catalogue Data Subsets referencing a URL
        corresponding to a metadata registration that
        is planned for deletion.
        """
        pass
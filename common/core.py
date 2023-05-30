from abc import ABC, abstractclassmethod

class AbstractOrganisationDatabaseQueries(ABC):
    pass

class AbstractIndividualDatabaseQueries(ABC):
    pass

class AbstractProjectDatabaseQueries(ABC):
    pass

class AbstractPlatformDatabaseQueries(ABC):
    pass

class AbstractOperationDatabaseQueries(ABC):
    pass

class AbstractInstrumentDatabaseQueries(ABC):
    @abstractclassmethod
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        """
        Instruments referencing at least one URL from
        a list of Instrument Type URLs.
        """
        pass

    @abstractclassmethod
    def for_search(self, instrument_type_urls: list):
        """
        Instruments referencing at least one URL
        from a list of Instrument Type URLs.
        """
        pass

class AbstractAcquisitionCapabilitiesDatabaseQueries(ABC):
    @abstractclassmethod
    def referencing_instrument_urls(self, instrument_urls: list):
        """
        Acquisition Capabilities referencing at least one URL from
        a list of Instrument URLs.
        """
        pass

    @abstractclassmethod
    def referencing_observed_property_urls(self, observed_property_urls: list):
        """
        Acquisition Capabilities referencing at least one URL from
        a list of Observed Property URLs.
        """
        pass

    @abstractclassmethod
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

class AbstractAcquisitionDatabaseQueries(ABC):
    @abstractclassmethod
    def referencing_acquisition_capability_set_urls(self, acquisition_capability_set_urls: list):
        """
        Acquisitions referencing at least one URL from
        a list of Acquisition Capabilities.
        """
        pass

    @abstractclassmethod
    def for_search(self, acquisition_capability_set_urls: list):
        """
        Acquisitions referencing at least one URL from a
        list of Acquisition Capabilities URLs.
        """
        pass

class AbstractComputationCapabilitiesDatabaseQueries(ABC):
    @abstractclassmethod
    def referencing_computation_type_urls(self, computation_type_urls: list):
        """
        Computation Capabilities matching at least one URL from a
        list of Computation Type URLs.
        """
        pass

    @abstractclassmethod
    def referencing_observed_property_urls(self, observed_property_urls: list):
        """
        Computation Capabilities matching at least one URL from a
        list of Observed Property URLs.
        """
        pass

    @abstractclassmethod
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

class AbstractComputationDatabaseQueries(ABC):
    @abstractclassmethod
    def referencing_computation_capability_set_urls(self, computation_capability_set_urls: list):
        """
        Computations referencing at least one URL from a list
        of Computation Capabilities by URL in the passed in list.
        """
        pass

    @abstractclassmethod
    def for_search(self, computation_capability_set_urls: list):
        """
        Computations referencing at least one URL from a list
        of Computation Capabilities URLs.
        """
        pass

class AbstractProcessDatabaseQueries(ABC):
    @abstractclassmethod
    def referencing_acquisition_urls(self, acquisition_urls: list):
        """
        Processes referencing at least one URL from a list
        of Acquisition URLs.
        """
        pass

    @abstractclassmethod
    def referencing_computation_urls(self, computation_urls: list):
        """
        Processes referencing at least one URL from a list
        of Computation URLs.
        """
        pass

    @abstractclassmethod
    def for_search(self, acquisition_urls: list, computation_urls: list):
        """
        Processes meeting at least one of the following criteria:
        * Referencing at least one URL from a list of Acquisition URLs
        * Referencing at least one URL from a list of Computation URLs
        """
        pass

class AbstractDataCollectionDatabaseQueries(ABC):
    @abstractclassmethod
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        """
        Data Collections referencing at least one URL
        from a list of Instrument Type URLs.
        """
        pass

    @abstractclassmethod
    def referencing_computation_type_urls(self, computation_type_urls: list):
        """
        Data Collections referencing at least one URL
        from a list of Computation Type URLs.
        """
        pass

    @abstractclassmethod
    def referencing_process_urls(self, process_urls: list):
        """
        Data Collections referencing at least one URL
        from a list of Process URLs.
        """
        pass

    @abstractclassmethod
    def referencing_feature_of_interest_urls(self, feature_of_interest_urls: list):
        """
        Data Collections referencing at least one URL
        from a list of Feature of Interest URLs.
        """
        pass

    @abstractclassmethod
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

class AbstractCatalogueDatabaseQueries(ABC):
    pass

class AbstractCatalogueEntryDatabaseQueries(ABC):
    pass

class AbstractCatalogueDataSubsetDatabaseQueries(ABC):
    pass
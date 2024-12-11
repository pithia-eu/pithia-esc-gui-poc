from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True)
class CapabilityLinkMetadataUpdate:
    platforms: Optional[list[str]] = field(default_factory=list)
    capabilities: Optional[str] = None
    standard_identifiers: Optional[list[str]] = field(default_factory=list)
    time_spans: Optional[list[str]] = field(default_factory=list)


@dataclass(kw_only=True)
class PithiaIdentifierMetadataUpdate:
    localid: Optional[str] = None
    namespace: Optional[str] = None
    version: Optional[str] = '1'
    creation_date: Optional[str] = None
    last_modification_date: Optional[str] = None


@dataclass(kw_only=True)
class ProcessCapabilityMetadataUpdate:
    name: Optional[str] = None
    observed_property: Optional[str] = None
    dimensionality_instance: Optional[str] = None
    dimensionality_timeline: Optional[str] = None
    cadence: Optional[str] = None
    cadence_unit: Optional[str] = None
    vector_representation: Optional[list[str]] = field(default_factory=list)
    coordinate_system: Optional[str] = None
    units: Optional[str] = None
    qualifier: Optional[list[str]] = field(default_factory=list)


@dataclass(kw_only=True)
class ContactInfoAddressMetadataUpdate:
    delivery_point: Optional[str] = None
    city: Optional[str] = None
    administrative_area: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    electronic_mail_address: Optional[str] = None


@dataclass(kw_only=True)
class CitationPropertyTypeMetadataUpdate:
    citation_title: Optional[str] = None
    citation_publication_date: Optional[str] = None
    citation_doi: Optional[str] = None
    citation_url: Optional[str] = None
    other_citation_details: Optional[str] = None


@dataclass(kw_only=True)
class ContactInfoMetadataUpdate:
    phone: Optional[str] = None
    address: Optional[ContactInfoAddressMetadataUpdate] = ContactInfoAddressMetadataUpdate()
    online_resource: Optional[str] = None
    hours_of_service: Optional[str] = None
    contact_instructions: Optional[str] = None


@dataclass(kw_only=True)
class DoiKernelMetadataUpdate:
    referent_doi_name: Optional[str] = None
    primary_referent_type: Optional[str] = None
    registration_agency_doi_name: Optional[str] = None
    doi_issue_date: Optional[str] = None
    doi_issue_number: Optional[int] = None
    rc_name_primary_language: Optional[str] = None
    rc_name_value: Optional[str] = None
    rc_name_type: Optional[str] = None
    rc_identifier_non_uri_value: Optional[str] = None
    rc_identifier_uri_return_type: Optional[str] = None
    rc_identifier_uri_value: Optional[str] = None
    rc_identifier_type: Optional[str] = None
    rc_structural_type: Optional[str] = None
    rc_mode: Optional[str] = None
    rc_character: Optional[str] = None
    rc_type: Optional[str] = None
    rc_principal_agent_name_value: Optional[str] = None
    rc_principal_agent_name_type: Optional[str] = None


@dataclass(kw_only=True)
class InputOutputMetadataUpdate:
    name: Optional[str] = None
    description: Optional[str] = None


@dataclass(kw_only=True)
class LocationMetadataUpdate:
    location_name: Optional[str] = None
    geometry_location_point_id: Optional[str] = None
    geometry_location_point_srs_name: Optional[str] = None
    geometry_location_point_pos_1: Optional[float] = None
    geometry_location_point_pos_2: Optional[float] = None


@dataclass(kw_only=True)
class TimePeriodMetadataUpdate:
    time_period_id: Optional[str] = None
    time_instant_begin_id: Optional[str] = None
    time_instant_begin_position: Optional[str] = None
    time_instant_end_id: Optional[str] = None
    time_instant_end_position: Optional[str] = None


class OperationTimeMetadataUpdate(TimePeriodMetadataUpdate):
    pass


class PhenomenonTimeMetadataUpdate(TimePeriodMetadataUpdate):
    pass


class ResultTimeMetadataUpdate(TimePeriodMetadataUpdate):
    pass


@dataclass(kw_only=True)
class RelatedPartyMetadataUpdate:
    role: Optional[str] = None
    parties: Optional[list[str]] = field(default_factory=list)


@dataclass(kw_only=True)
class SourceMetadataUpdate:
    service_functions: Optional[list[str]] = field(default_factory=list)
    linkage: Optional[str] = None
    name: Optional[str] = None
    protocol: Optional[str] = None
    description: Optional[str] = None
    data_formats: Optional[list[str]] = field(default_factory=list)

@dataclass(kw_only=True)
class CatalogueDataSubsetSourceMetadataUpdate(SourceMetadataUpdate):
    file_input_name: Optional[str] = None

@dataclass(kw_only=True)
class CatalogueDataSubsetSourceWithExistingDataHubFileMetadataUpdate(CatalogueDataSubsetSourceMetadataUpdate):
    is_existing_datahub_file_used: Optional[bool] = False


@dataclass(kw_only=True)
class StandardIdentifierMetadataUpdate:
    authority: Optional[str] = None
    value: Optional[str] = None


@dataclass(kw_only=True)
class TimeSpanMetadataUpdate:
    begin_position: Optional[str] = None
    end_position: Optional[str] = None
import copy

# Organisation
ORGANISATION_PROPERTIES_FULL = {
    'localid': 'Organisation_Test',
    'namespace': 'test',
    'name': 'Organisation Test',
    'identifier_version': '1',
    'short_name': 'OTD',
    'description': 'Organisation Test description',
    'contact_info': {
        'phone': '12345',
        'address': {
            'delivery_point': 'alpha',
            'city': 'london',
            'administrative_area': 'harrow',
            'postal_code': 'abc 789',
            'country': 'UK',
            'electronic_mail_address': 'test@email.com',
        },
        'online_resource': 'http://test.test.edu',
        'hours_of_service': '0:00am-0:00am',
        'contact_instructions': 'Contact by email or phone',
    },
}

def _blank_out_string_properties_of_dict(property_dict):
    for key in property_dict:
        if isinstance(property_dict[key], dict):
            _blank_out_string_properties_of_dict(property_dict[key])
            continue
        property_dict[key] = ''

ORGANISATION_PROPERTIES_NO_CONTACT_INFO = copy.deepcopy(ORGANISATION_PROPERTIES_FULL)
_blank_out_string_properties_of_dict(ORGANISATION_PROPERTIES_NO_CONTACT_INFO['contact_info'])

ORGANISATION_PROPERTIES_PARTIAL_CONTACT_INFO = copy.deepcopy(ORGANISATION_PROPERTIES_NO_CONTACT_INFO)
ORGANISATION_PROPERTIES_PARTIAL_CONTACT_INFO['contact_info']['address'] = ORGANISATION_PROPERTIES_FULL['contact_info']['address']
ORGANISATION_PROPERTIES_PARTIAL_CONTACT_INFO['contact_info']['hours_of_service'] = ORGANISATION_PROPERTIES_FULL['contact_info']['hours_of_service']

ORGANISATION_PROPERTIES_NO_ADDRESS = copy.deepcopy(ORGANISATION_PROPERTIES_FULL)
_blank_out_string_properties_of_dict(ORGANISATION_PROPERTIES_NO_ADDRESS['contact_info']['address'])

ORGANISATION_PROPERTIES_PARTIAL_ADDRESS = copy.deepcopy(ORGANISATION_PROPERTIES_NO_ADDRESS)
ORGANISATION_PROPERTIES_PARTIAL_ADDRESS['contact_info']['address']['delivery_point'] = ORGANISATION_PROPERTIES_FULL['contact_info']['address']['delivery_point']

# Individual
INDIVIDUAL_PROPERTIES_FULL = {
    'localid': 'Individual_Test',
    'namespace': 'test',
    'name': 'Individual Test',
    'identifier_version': '1',
    'contact_info': {
        'phone': '12345',
        'address': {
            'delivery_point': 'alpha',
            'city': 'london',
            'administrative_area': 'harrow',
            'postal_code': 'abc 789',
            'country': 'UK',
            'electronic_mail_address': 'test@email.com'
        },
        'online_resource': 'http://test.test.edu',
        'hours_of_service': '0:00am-0:00am',
        'contact_instructions': 'Contact by email or phone',
    },
    'position_name': 'CEO',
    'organisation': 'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
}

INDIVIDUAL_PROPERTIES_NO_CONTACT_INFO = copy.deepcopy(INDIVIDUAL_PROPERTIES_FULL)
_blank_out_string_properties_of_dict(INDIVIDUAL_PROPERTIES_NO_CONTACT_INFO['contact_info'])

# Project
PROJECT_PROPERTIES_FULL = {
    'localid': 'Project_Test',
    'namespace': 'test',
    'name': 'Project Test',
    'short_name': 'Project Test short name',
    'identifier_version': '1',
    'description': 'Description',
    'abstract': 'Abstract',
    'url': 'https://www.example.com/',
    'documentation': {
        'citation_title': 'citation',
        'citation_date': '1997-01-01',
        'ci_date_type_code': 'Publication date',
        'ci_date_type_code_code_list': 'something',
        'ci_date_type_code_code_list_value': 'something else',
        'ci_linkage_url': 'https://www.example.com/',
        'other_citation_details': 'other citation details',
        'doi': 'abc',
    },
    'keyword_dict_list': [
        {
            'keywords': [
                'Keyword 1',
                'Keyword 2',
                'Keyword 3',
                'Keyword 4',
                'Keyword 5',
            ],
            'type': {
                'code_list': "#test1",
                'code_list_value': "Test"
            },
        },
        {
            'keywords': [
                'Keyword 1A',
                'Keyword 2A',
                'Keyword 3A',
                'Keyword 4A',
                'Keyword 5A',
            ],
            'type': {
                'code_list': "#test1a",
                'code_list_value': "Testa",
            },
        },
    ],
    'related_parties': [
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'parties': [
                'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
                'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
            ],
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'parties': ['https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test'],
        },
    ],
    'status': 'https://metadata.pithia.eu/ontology/2.2/status/OnGoing',
}

PROJECT_PROPERTIES_NO_CITATION_TITLE = copy.deepcopy(PROJECT_PROPERTIES_FULL)
PROJECT_PROPERTIES_NO_CITATION_TITLE['documentation']['citation_title'] = ''

PROJECT_PROPERTIES_NO_CITATION_DATE = copy.deepcopy(PROJECT_PROPERTIES_FULL)
PROJECT_PROPERTIES_NO_CITATION_DATE['documentation']['citation_date'] = ''

# Platform
PLATFORM_PROPERTIES_FULL = {
    'localid': 'Platform_Test',
    'namespace': 'test',
    'name': 'Platform Test',
    'short_name': 'PT',
    'identifier_version': '1',
    'standard_identifiers': [
        {
            'authority': 'authority1',
            'value': 'ABC123',
        },
        {
            'authority': 'authority2',
            'value': 'DEF456',
        },
    ],
    'url': 'https://www.example.com/',
    'description': 'Platform description',
    'type': 'https://metadata.pithia.eu/ontology/2.2/instrumentType/AssimilativeModel/',
    'documentation': {
        'citation_title': 'citation',
        'citation_date': '1997-01-01',
        'ci_date_type_code': 'Publication date',
        'ci_date_type_code_code_list': 'something',
        'ci_date_type_code_code_list_value': 'something else',
        'ci_linkage_url': 'https://www.example.com/',
        'other_citation_details': 'other citation details',
        'doi': 'abc',
    },
    'location': {
        'geometry_location': {
            'point': {
                'id': 'n11',
                'srs_name': 'https://metadata.pithia.eu/ontology/2.2/crs/WGS84spherical',
                'pos': ''
            },
        },
        'name_location': {
            'code': 'Polar orbit in the magnetosphere and solar wind'
        },
    },
    'related_parties': [
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'parties': [
                'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
                'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
            ],
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'parties': ['https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test'],
        },
    ],
    'child_platforms': [
        'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test',
    ],
}
PLATFORM_PROPERTIES_NO_URL = copy.deepcopy(PLATFORM_PROPERTIES_FULL)
PLATFORM_PROPERTIES_NO_URL['url'] = ''

PLATFORM_PROPERTIES_NO_GEOMETRY_LOCATION = copy.deepcopy(PLATFORM_PROPERTIES_FULL)
_blank_out_string_properties_of_dict(PLATFORM_PROPERTIES_NO_GEOMETRY_LOCATION['location']['geometry_location']['point'])

# Operation
OPERATION_PROPERTIES_FULL = {
    'localid': 'Operation_Test',
    'namespace': 'test',
    'name': 'Operation Test',
    'identifier_version': '1',
    'description': 'Operation description',
    'location': {
        'geometry_location': {
            'point': {
                'id': 'n11',
                'srs_name': 'https://metadata.pithia.eu/ontology/2.2/crs/WGS84spherical',
                'pos': ''
            },
        },
        'name_location': {
            'code': 'Polar orbit in the magnetosphere and solar wind'
        },
    },
    'operation_time': {
        'time_period': {
            'id': 't_esr_dsnd',
            'begin': {
                'time_instant': {
                    'id': 'ti1',
                    'time_position': '2000-03-07',
                }
            },
            'end': {
                'time_instant': {
                    'id': 'ti2',
                    'time_position': '2050-12-31',
                }
            },
        },
    },
    'documentation': {
        'citation_title': 'citation',
        'citation_date': '1997-01-01',
        'ci_date_type_code': 'Publication date',
        'ci_date_type_code_code_list': 'something',
        'ci_date_type_code_code_list_value': 'something else',
        'ci_linkage_url': 'https://www.example.com/',
        'other_citation_details': 'other citation details',
        'doi': 'abc',
    },
    'status': 'https://metadata.pithia.eu/ontology/2.2/status/OnGoing',
    'related_parties': [
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'parties': [
                'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
                'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
            ],
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'parties': ['https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test'],
        },
    ],
    'platforms': ['https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test'],
    'child_operations': ['https://metadata.pithia.eu/resources/2.2/operation/test/Operation_Test'],
}

# Instrument
INSTRUMENT_PROPERTIES_FULL = {
    'localid': 'Instrument_Test',
    'namespace': 'test',
    'name': 'Instrument Test',
    'identifier_version': '1',
    'description': 'Description',
    'version': '1',
    'type': 'https://metadata.pithia.eu/ontology/2.2/instrumentType/AssimilativeModel/',
    'operational_modes': [
        {
            'id': 'instrumentoperationalmode1',
            'name': 'Instrument Operational Mode 1',
            'description': 'operational mode 1 description',
        },
        {
            'id': 'instrumentoperationalmode2',
            'name': 'Instrument Operational Mode 2',
            'description': 'operational mode 2 description',
        },
    ],
    'url': 'https://www.example.com/',
    'documentation': {
        'citation_title': 'citation',
        'citation_date': '1997-01-01',
        'ci_date_type_code': 'Publication date',
        'ci_date_type_code_code_list': 'something',
        'ci_date_type_code_code_list_value': 'something else',
        'ci_linkage_url': 'https://www.example.com/',
        'other_citation_details': 'other citation details',
        'doi': 'abc',
    },
    'related_parties': [
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'parties': [
                'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
                'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
            ],
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'parties': ['https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test'],
        },
    ],
    'members': [
        'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test',
        'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_2',
        'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_3',
    ],
}
INSTRUMENT_PROPERTIES_NO_TYPE = copy.deepcopy(INSTRUMENT_PROPERTIES_FULL)
INSTRUMENT_PROPERTIES_NO_TYPE['type'] = ''

# Acquisition Capabilities
ACQUISITION_CAPABILITIES_PROPERTIES_FULL = {
    'localid': 'AcquisitionCapabilities_Test',
    'namespace': 'test',
    'name': 'Acquisition Capabilities Test',
    'identifier_version': '1',
    'description': 'Description',
    'documentation': {
        'citation_title': 'citation',
        'citation_date': '1997-01-01',
        'ci_date_type_code': 'Publication date',
        'ci_date_type_code_code_list': 'something',
        'ci_date_type_code_code_list_value': 'something else',
        'ci_linkage_url': 'https://www.example.com/',
        'other_citation_details': 'other citation details',
        'doi': 'abc',
    },
    'capabilities': [
        {
            'name': 'Signal Strength',
            'observed_property': 'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'dimensionality_instance': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram',
            'dimensionality_timeline': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation',
            'cadence': '10.0',
            'cadence_units': 'minute',
            'vector_representation': [
                'https://metadata.pithia.eu/ontology/2.2/component/D'
            ],
            'coordinate_system': 'https://metadata.pithia.eu/ontology/2.2/crs/CGM',
            'units': 'https://metadata.pithia.eu/ontology/2.2/unit/dB',
            'qualifier': [
                'https://metadata.pithia.eu/ontology/2.2/qualifier/Approximation'
            ],
        },
        {
            'name': 'Signal Strength',
            'observed_property': 'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'dimensionality_instance': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram',
            'dimensionality_timeline': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation',
            'cadence': '120.0',
            'cadence_units': 'year',
            'vector_representation': [
                'https://metadata.pithia.eu/ontology/2.2/component/E'
            ],
            'coordinate_system': 'https://metadata.pithia.eu/ontology/2.2/crs/GEOcartesian',
            'units': 'https://metadata.pithia.eu/ontology/2.2/unit/dB',
            'qualifier': [
                'https://metadata.pithia.eu/ontology/2.2/qualifier/Derived'
            ],
        },
    ],
    'data_levels': [
        'https://metadata.pithia.eu/ontology/2.2/dataLevel/L1',
        'https://metadata.pithia.eu/ontology/2.2/dataLevel/L2',
    ],
    'quality_assessment': {
        'data_quality_flags': [
            'https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ0',
        ],
        'metadata_quality_flags': [
            'https://metadata.pithia.eu/ontology/2.2/metadataQualityFlag/MQ1',
        ],
    },
    'instrument_mode_pair': {
        'instrument': 'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test',
        'mode': 'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test#instrumentoperationalmode1',
    },
    'input_name': 'input name',
    'input_description': 'input description',
    'output_name': 'output name',
    'output_description': 'output description',
    'related_parties': [
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'parties': [
                'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
                'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
            ],
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'parties': ['https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test'],
        },
    ],
}
ACQUISITION_CAPABILITIES_BLANK_CADENCE_UNIT = copy.deepcopy(ACQUISITION_CAPABILITIES_PROPERTIES_FULL)
ACQUISITION_CAPABILITIES_BLANK_CADENCE_UNIT['capabilities'][0]['cadence_units'] = ''

# Acquisition
ACQUISITION_PROPERTIES_FULL = {
    'localid': 'Acquisition_Test',
    'namespace': 'test',
    'name': 'Acquisition Test',
    'identifier_version': '1',
    'description': 'Description',
    'capability_links': [
        {
            'platforms': [
                'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test'
            ],
            'standard_identifiers': [
                {
                    'authority': 'URSI',
                    'value': 'AT138',
                }
            ],
            'acquisition_capabilities': 'https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test',
            'time_spans': [],
        },
        {
            'platforms': [
                'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test'
            ],
            'standard_identifiers': [
                {
                    'authority': 'URSI',
                    'value': 'AT138',
                }
            ],
            'acquisition_capabilities': 'https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test',
            'time_spans': [
                {
                    'begin_position': '10-06-2020',
                    'end_position': 'before',
                },
                {
                    'begin_position': '01-01-2020',
                    'end_position': 'after',
                },
            ],
        },
    ],
}
ACQUISITION_PROPERTIES_WITH_BLANK_ACQ_CAPS = copy.deepcopy(ACQUISITION_PROPERTIES_FULL)
ACQUISITION_PROPERTIES_WITH_BLANK_ACQ_CAPS['capability_links'][0]['acquisition_capabilities'] = ''

# Computation Capabilities
COMPUTATION_CAPABILITIES_PROPERTIES_FULL = {
    'localid': 'ComputationCapabilities_Test',
    'namespace': 'test',
    'name': 'Computation Capabilities Test',
    'identifier_version': '1',
    'description': 'Description',
    'capabilities': [
        {
            'name': 'Signal Strength',
            'observed_property': 'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'dimensionality_instance': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram',
            'dimensionality_timeline': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation',
            'cadence': '10.0',
            'cadence_units': 'minute',
            'vector_representation': [
                'https://metadata.pithia.eu/ontology/2.2/component/D'
            ],
            'coordinate_system': 'https://metadata.pithia.eu/ontology/2.2/crs/CGM',
            'units': 'https://metadata.pithia.eu/ontology/2.2/unit/dB',
            'qualifier': [
                'https://metadata.pithia.eu/ontology/2.2/qualifier/Approximation'
            ],
        },
        {
            'name': 'Signal Strength',
            'observed_property': 'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'dimensionality_instance': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram',
            'dimensionality_timeline': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation',
            'cadence': '10.0',
            'cadence_units': 'minute',
            'vector_representation': [
                'https://metadata.pithia.eu/ontology/2.2/component/D'
            ],
            'coordinate_system': 'https://metadata.pithia.eu/ontology/2.2/crs/CGM',
            'units': 'https://metadata.pithia.eu/ontology/2.2/unit/dB',
            'qualifier': [
                'https://metadata.pithia.eu/ontology/2.2/qualifier/Approximation'
            ],
        },
    ],
    'data_levels': ['https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V'],
    'type': 'https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual',
    'quality_assessment': {
        'data_quality_flags': [
            'https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ0',
        ],
        'metadata_quality_flags': [
            'https://metadata.pithia.eu/ontology/2.2/metadataQualityFlag/MQ1',
        ],
    },
    'child_computations': [
        'https://metadata.pithia.eu/resources/2.2/computationCapabilities/pithia/ComputationCapabilities_IonogramScaling_StandardChars_Basic',
        'https://metadata.pithia.eu/resources/2.2/computationCapabilities/pithia/ComputationCapabilities_IonogramScaling_StandardChars_Advanced',
    ]
}

# Computation
COMPUTATION_PROPERTIES_FULL = {
    'localid': 'Computation_Test',
    'namespace': 'test',
    'name': 'Computation Test',
    'identifier_version': '1',
    'description': 'Description',
    'capability_links': [
        {
            'platforms': [
                'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test'
            ],
            'standard_identifiers': [
                {
                    'authority': 'URSI',
                    'value': 'AT138',
                }
            ],
            'computation_capabilities': 'https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test',
            'time_spans': [],
        },
        {
            'platforms': [
                'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test'
            ],
            'standard_identifiers': [
                {
                    'authority': 'URSI',
                    'value': 'AT138',
                }
            ],
            'computation_capabilities': 'https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test',
            'time_spans': [
                {
                    'begin_position': '10-06-2020',
                    'end_position': 'before',
                },
                {
                    'begin_position': '01-01-2020',
                    'end_position': 'after',
                },
            ],
        },
    ],
}

# Process
PROCESS_PROPERTIES_FULL = {
    'localid': 'Process_Test',
    'namespace': 'test',
    'name': 'Process Test',
    'identifier_version': '1',
    'description': 'Description',
    'data_levels': [
        'https://metadata.pithia.eu/ontology/2.2/dataLevel/L1',
        'https://metadata.pithia.eu/ontology/2.2/dataLevel/L2',
    ],
    'quality_assessment': {
        'data_quality_flags': [
            'https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ0',
        ],
        'metadata_quality_flags': [
            'https://metadata.pithia.eu/ontology/2.2/metadataQualityFlag/MQ1',
        ],
    },
    'acquisition': 'https://metadata.pithia.eu/resources/2.2/acquisition/test/Acquisition_Test',
    'computation': 'https://metadata.pithia.eu/resources/2.2/computation/test/Computation_Test',
}

# Data Collection
DATA_COLLECTION_PROPERTIES_FULL = {
    'localid': 'DataCollection_Test',
    'namespace': 'test',
    'name': 'Data Collection Test',
    'identifier_version': '1',
    'description': 'Description',
    'process': 'https://metadata.pithia.eu/resources/2.2/process/test/CompositeProcess_Test',
    'features_of_interest': [
        'https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_F-Region_Bottomside',
        'https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_E-Region',
    ],
    'type': 'https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder',
    'project': 'https://metadata.pithia.eu/resources/2.2/project/test/Project_Test',
    'related_parties': [
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'parties': [
                'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
                'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
            ],
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'parties': ['https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test'],
        },
    ],
    'collection_results': [
        {
            'service_function': 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download',
            'linkage': 'https://giro.uml.edu/didbase/',
            'name': 'Online Resource 1',
            'protocol': 'HTTPS',
            'description': 'Lorem ipsum dolor sit amet',
            'data_format': 'https://metadata.pithia.eu/ontology/2.2/resultDataFormat/image-png',
        },
        {
            'service_function': 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download',
            'linkage': 'https://ulcar.uml.edu/SAO-X/',
            'name': 'Online Resource 2',
            'protocol': 'HTTPS',
            'description': 'Lorem ipsum dolor sit amet',
            'data_format': 'https://metadata.pithia.eu/ontology/2.2/resultDataFormat/image-png',
        },
    ],
    'data_levels': [
        'https://metadata.pithia.eu/ontology/2.2/dataLevel/L0',
        'https://metadata.pithia.eu/ontology/2.2/dataLevel/L1',
        'https://metadata.pithia.eu/ontology/2.2/dataLevel/L2A',
    ],
    'quality_assessment': {
        'data_quality_flags': [
            'https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ2',
        ],
    },
    'permissions': [
        'https://metadata.pithia.eu/ontology/2.2/licence/LGDC_SpaceDataPolicies',
    ]
}

# Catalogue
CATALOGUE_PROPERTIES_FULL = {
    'localid': 'Catalogue_Test',
    'namespace': 'test',
    'name': 'Catalogue Test',
    'identifier_version': '1',
    'description': 'Description',
    'catalogue_category': 'https://metadata.pithia.eu/ontology/2.2/computationType/Model',
}

# Catalogue Entry
CATALOGUE_ENTRY_PROPERTIES_FULL = {
    'localid': 'Catalogue_Entry_Test',
    'namespace': 'test',
    'entry_name': 'Catalogue Entry Test',
    'identifier_version': '1',
    'entry_description': 'Entry description',
    'phenomenon_time': {
        'time_period': {
            'id': 't_esr_dsnd',
            'begin': {
                'time_instant': {
                    'id': 'ti1',
                    'time_position': '2000-03-07',
                }
            },
            'end': {
                'time_instant': {
                    'id': 'ti2',
                    'time_position': '2050-12-31',
                }
            },
        },
    },
}

# Catalogue Data Subset
CATALOGUE_DATA_SUBSET_PROPERTIES_FULL = {
    'localid': 'Catalogue_Data_Subset_Test',
    'namespace': 'test',
    'data_subset_name': 'Catalogue Data Subset Test',
    'identifier_version': '1',
    'data_subset_description': 'Catalogue data subset description',
    'data_collection': 'https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test',
    'result_time': {
        'time_period': {
            'id': 't_esr_dsnd',
            'begin': {
                'time_instant': {
                    'id': 'ti1',
                    'time_position': '2000-03-07',
                }
            },
            'end': {
                'time_instant': {
                    'id': 'ti2',
                    'time_position': '2050-12-31',
                }
            },
        },
    },
    'sources': [
        {
            'service_function': 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download',
            'linkage': 'https://giro.uml.edu/didbase/',
            'name': 'Online Resource 1',
            'protocol': 'HTTPS',
            'description': 'Lorem ipsum dolor sit amet',
            'data_format': 'https://metadata.pithia.eu/ontology/2.2/resultDataFormat/image-png',
        },
        {
            'service_function': 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download',
            'linkage': 'https://ulcar.uml.edu/SAO-X/',
            'name': 'Online Resource 2',
            'protocol': 'HTTPS',
            'description': 'Lorem ipsum dolor sit amet',
            'data_format': 'https://metadata.pithia.eu/ontology/2.2/resultDataFormat/image-png',
        },
    ],
    'data_levels': [
        'https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V',
    ],
    'quality_assessment': {
        'data_quality_flags': [
            'https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3',
        ],
    },
}

WORKFLOW_PROPERTIES_FULL = {
    'localid': 'Workflow_Test',
    'namespace': 'test',
    'name': 'Workflow Test',
    'identifier_version': '3',
    'description': 'Workflow description',
    'data_collections': [
        'https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test_1',
        'https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test_2',
    ],
    'workflow_details': 'https://www.example.com/',
}
WORKFLOW_PROPERTIES_NO_DATA_COLLECTIONS = copy.deepcopy(WORKFLOW_PROPERTIES_FULL)
WORKFLOW_PROPERTIES_NO_DATA_COLLECTIONS['data_collections'] = []

WORKFLOW_PROPERTIES_NO_WORKFLOW_DETAILS = copy.deepcopy(WORKFLOW_PROPERTIES_FULL)
WORKFLOW_PROPERTIES_NO_WORKFLOW_DETAILS['workflow_details'] = ''
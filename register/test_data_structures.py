# Organisation
ORGANISATION_PROPERTIES = {
    'local_id': 'Organisation_Test',
    'namespace': 'test',
    'name': 'Organisation Test',
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

# Individual
INDIVIDUAL_PROPERTIES = {
    'local_id': 'Individual_Test',
    'namespace': 'test',
    'name': 'Individual Test',
    'description': 'Description',
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

# Project
PROJECT_PROPERTIES = {
    'local_id': 'Project_Test',
    'namespace': 'test',
    'name': 'Project Test',
    'description': 'Description',
    'abstract': 'Abstract',
    'url': 'https://www.example.com/',
    'documentation': {
        'citation_title': 'citation',
        'citation_date': 'citation date',
        'ci_date_type_code': 'Publication List',
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
            'party': 'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'party': 'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
        },
    ],
    'status': 'https://metadata.pithia.eu/ontology/2.2/status/OnGoing',
}

# Platform
PLATFORM_PROPERTIES = {
    'local_id': 'Platform_Test',
    'namespace': 'test',
    'name': 'Platform Test',
    'short_name': 'PT',
    'description': 'Platform description',
    'type': 'https://metadata.pithia.eu/ontology/2.2/instrumentType/AssimilativeModel/',
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
            'party': 'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'party': 'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
        },
    ],
}

# Operation
OPERATION_PROPERTIES = {
    'local_id': 'Operation_Test',
    'namespace': 'test',
    'name': 'Operation Test',
    'description': 'Operation description',
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
    'status': 'https://metadata.pithia.eu/ontology/2.2/status/OnGoing',
    'related_parties': [
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'party': 'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'party': 'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
        },
    ],
    'platform': 'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test',
}

# Instrument
INSTRUMENT_PROPERTIES = {
    'local_id': 'Instrument_Test',
    'namespace': 'test',
    'name': 'Instrument Test',
    'description': 'Description',
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
    'related_parties': [
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'party': 'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'party': 'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
        },
    ],
}

# Acquisition Capabilities
ACQUISITION_CAPABILITIES_PROPERTIES = {
    'local_id': 'AcquisitionCapabilities_Test',
    'namespace': 'test',
    'name': 'Acquisition Capabilities Test',
    'description': 'Description',
    'capabilities': [
        {
            'name': 'Signal Strength',
            'observed_property': 'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'dimensionality_instance': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram',
            'dimensionality_timeline': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation',
            'units': 'https://metadata.pithia.eu/ontology/2.2/unit/dB',
        },
        {
            'name': 'Signal Strength',
            'observed_property': 'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'dimensionality_instance': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram',
            'dimensionality_timeline': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation',
            'units': 'https://metadata.pithia.eu/ontology/2.2/unit/dB',
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
}

# Acquisition
ACQUISITION_PROPERTIES = {
    'local_id': 'Acquisition_Test',
    'namespace': 'test',
    'name': 'Acquisition Test',
    'description': 'Description',
    'capability_links': [
        {
            'platform': 'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test',
            'standard_identifier': {
                'authority': 'URSI',
                'value': 'AT138',
            },
            'acquisition_capabilities': 'https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test',
        },
        {
            'platform': 'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test',
            'standard_identifier': {
                'authority': 'URSI',
                'value': 'AT138',
            },
            'acquisition_capabilities': 'https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test',
        },
    ],
}

# Computation Capabilities
COMPUTATION_CAPABILITIES_PROPERTIES = {
    'local_id': 'ComputationCapabilities_Test',
    'namespace': 'test',
    'name': 'Computation Capabilities Test',
    'description': 'Description',
    'capabilities': [
        {
            'name': 'Signal Strength',
            'observed_property': 'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'dimensionality_instance': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram',
            'dimensionality_timeline': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation',
            'units': 'https://metadata.pithia.eu/ontology/2.2/unit/dB',
        },
        {
            'name': 'Signal Strength',
            'observed_property': 'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'dimensionality_instance': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram',
            'dimensionality_timeline': 'https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation',
            'units': 'https://metadata.pithia.eu/ontology/2.2/unit/dB',
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
COMPUTATION_PROPERTIES = {
    'local_id': 'Computation_Test',
    'namespace': 'test',
    'name': 'Computation Test',
    'description': 'Description',
    'capability_links': [
        {
            'platform': 'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test',
            'standard_identifier': {
                'authority': 'URSI',
                'value': 'AT138',
            },
            'computation_capabilities': 'https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test',
        },
        {
            'platform': 'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test',
            'standard_identifier': {
                'authority': 'URSI',
                'value': 'AT138',
            },
            'computation_capabilities': 'https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test',
        },
    ],
}

# Process
PROCESS_PROPERTIES = {
    'local_id': 'Process_Test',
    'namespace': 'test',
    'name': 'Process Test',
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
DATA_COLLECTION_PROPERTIES = {
    'local_id': 'DataCollection_Test',
    'namespace': 'test',
    'name': 'Data Collection Test',
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
            'party': 'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
        },
        {
            'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
            'party': 'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
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
CATALOGUE_PROPERTIES = {
    'local_id': 'Catalogue_Test',
    'namespace': 'test',
    'name': 'Catalogue Test',
    'description': 'Description',
    'catalogue_category': 'https://metadata.pithia.eu/ontology/2.2/computationType/Model',
}

# Catalogue Entry
CATALOGUE_ENTRY_PROPERTIES = {
    'local_id': 'Catalogue_Entry_Test',
    'namespace': 'test',
    'entry_name': 'Catalogue Entry Test',
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
CATALOGUE_DATA_SUBSET_PROPERTIES = {
    'local_id': 'Catalogue_Data_Subset_Test',
    'namespace': 'test',
    'data_subset_name': 'Catalogue Data Subset Test',
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

WORKFLOW_PROPERTIES = {
    'local_id': 'Workflow_Test',
    'namespace': 'test',
    'name': 'Workflow Test',
    'description': 'Workflow description',
    'data_collections': [
        'https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test_1',
        'https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test_2',
    ],
    'workflow_details': '',
}
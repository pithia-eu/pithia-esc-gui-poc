# Metadata server URL bases
PITHIA_METADATA_SERVER_URL_BASE_NO_VERSION = 'metadata.pithia.eu/resources'
PITHIA_METADATA_SERVER_URL_BASE = f'{PITHIA_METADATA_SERVER_URL_BASE_NO_VERSION}/2.2'
PITHIA_METADATA_SERVER_HTTPS_URL_BASE = f'https://{PITHIA_METADATA_SERVER_URL_BASE}'
# Space Physics Ontology URL bases
SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE_NO_VERSION = 'metadata.pithia.eu/ontology'
SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE_NO_VERSION}/2.2'
SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE = f'https://{SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE}'
# URL bases for Space Physics Ontology categories
# used in Search Data Collections by Content.
ANNOTATION_TYPE_URL_BASE = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/annotationType'
COMPUTATION_TYPE_URL_BASE = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/computationType'
FEATURE_OF_INTEREST_URL_BASE = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/featureOfInterest'
INSTRUMENT_TYPE_URL_BASE = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/instrumentType'
OBSERVED_PROPERTY_URL_BASE = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/observedProperty'
# Static dataset
STATIC_DATASET_TYPE_READABLE = 'static dataset'
STATIC_DATASET_TYPE_PLURAL_READABLE = 'static datasets'
STATIC_DATASET_TYPE_DESCRIPTION = '''A listing of events or investigations assembled to
    aid users in locating data of interest. Each Entry
    in a Static Dataset has distinct begin and end times
    and a list of registered Data Subsets with optional
    DOIs to their persistent storage.'''
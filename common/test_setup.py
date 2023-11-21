from . import test_xml_files
from .models import (
    Acquisition,
    AcquisitionCapabilities,
    Catalogue,
    CatalogueDataSubset,
    CatalogueEntry,
    Computation,
    ComputationCapabilities,
    DataCollection,
    Individual,
    Instrument,
    Operation,
    Organisation,
    Platform,
    Process,
    Project,
)

# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'

def _register_metadata_file_for_test(xml_file, model, user_id=SAMPLE_USER_ID, institution_id=SAMPLE_INSTITUTION_ID):
    xml_file.seek(0)
    return model.objects.create_from_xml_string(xml_file.read(), user_id, institution_id)

def register_organisation_for_test():
    return _register_metadata_file_for_test(test_xml_files.ORGANISATION_METADATA_XML, Organisation)

def register_individual_for_test():
    return _register_metadata_file_for_test(test_xml_files.INDIVIDUAL_METADATA_XML, Individual)

def register_project_for_test():
    return _register_metadata_file_for_test(test_xml_files.PROJECT_METADATA_XML, Project)

def register_platform_for_test():
    return _register_metadata_file_for_test(test_xml_files.PLATFORM_METADATA_XML, Platform)

def register_platform_with_child_platforms_for_test():
    return _register_metadata_file_for_test(test_xml_files.PLATFORM_WITH_CHILD_PLATFORMS_METADATA_XML, Platform)

def register_operation_for_test():
    return _register_metadata_file_for_test(test_xml_files.OPERATION_METADATA_XML, Operation)

def register_instrument_for_test():
    return _register_metadata_file_for_test(test_xml_files.INSTRUMENT_METADATA_XML, Instrument)

def register_acquisition_capabilities_for_test():
    return _register_metadata_file_for_test(test_xml_files.ACQUISITION_CAPABILITIES_METADATA_XML, AcquisitionCapabilities)

def register_acquisition_for_test():
    return _register_metadata_file_for_test(test_xml_files.ACQUISITION_METADATA_XML, Acquisition)

def register_acquisition_with_instrument_for_test():
    return _register_metadata_file_for_test(test_xml_files.ACQUISITION_WITH_INSTRUMENT_METADATA_XML, Acquisition)

def register_computation_capabilities_for_test():
    return _register_metadata_file_for_test(test_xml_files.COMPUTATION_CAPABILITIES_METADATA_XML, ComputationCapabilities)

def register_computation_capabilities_2_for_test():
    return _register_metadata_file_for_test(test_xml_files.COMPUTATION_CAPABILITIES_2_METADATA_XML, ComputationCapabilities)

def register_computation_for_test():
    return _register_metadata_file_for_test(test_xml_files.COMPUTATION_METADATA_XML, Computation)

def register_process_for_test():
    return _register_metadata_file_for_test(test_xml_files.PROCESS_METADATA_XML, Process)

def register_data_collection_for_test():
    return _register_metadata_file_for_test(test_xml_files.DATA_COLLECTION_METADATA_XML, DataCollection)

def register_catalogue_for_test():
    return _register_metadata_file_for_test(test_xml_files.CATALOGUE_METADATA_XML, Catalogue)

def register_catalogue_entry_for_test():
    return _register_metadata_file_for_test(test_xml_files.CATALOGUE_ENTRY_METADATA_XML, CatalogueEntry)

def register_catalogue_data_subset_for_test():
    return _register_metadata_file_for_test(test_xml_files.CATALOGUE_DATA_SUBSET_METADATA_XML, CatalogueDataSubset)

def register_all_metadata_types():
    register_organisation_for_test()
    register_individual_for_test()
    register_project_for_test()
    register_platform_for_test()
    register_operation_for_test()
    register_instrument_for_test()
    register_acquisition_capabilities_for_test()
    register_acquisition_for_test()
    register_computation_capabilities_for_test()
    register_computation_for_test()
    register_process_for_test()
    register_data_collection_for_test()
    register_catalogue_for_test()
    register_catalogue_entry_for_test()
    register_catalogue_data_subset_for_test()
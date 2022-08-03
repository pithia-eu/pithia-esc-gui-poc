import re
from register import mongodb_models, xml_conversion_checks_and_fixes
from validation import validation

ONTOLOGY_COMPONENT_ENUMS = {
    'computationType': 'computationTypes',
    'featureOfInterest': 'featuresOfInterest',
    'instrumentType': 'instrumentTypes',
    'measurand': 'measurands',
    'observedProperty': 'observedProperties',
    'phenomenon': 'phenomenons',
}

def convert_list_to_regex_list(list):
    return [re.compile(x) for x in list]

def map_ontology_components_to_local_ids(list):
    local_ids_list = []
    for x in list:
        local_ids_list.append(x['identifier']['pithia:Identifier']['localID'])
    return local_ids_list

def remove_underscore_from_id_attribute(resource):
    resource['id'] = resource['_id']
    return resource

def get_view_helper_variables_by_url_namespace(url_namespace):
    current_version_mongodb_model = None
    resource_revision_mongodb_model = None
    validation_function = None
    conversion_validation_and_fixing_function = None
    resource_type = ''
    resource_type_plural = ''
    if 'organisation' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentOrganisation
        resource_revision_mongodb_model = mongodb_models.OrganisationRevision
        validation_function = validation.validate_organisation_metadata_xml_file
        resource_type = 'Organisation'
        resource_type_plural = 'Organisations'
    if 'individual' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentIndividual
        resource_revision_mongodb_model = mongodb_models.IndividualRevision
        validation_function = validation.validate_individual_metadata_xml_file
        resource_type = 'Individual'
        resource_type_plural = 'Individuals'
    if 'project' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentProject
        resource_revision_mongodb_model = mongodb_models.ProjectRevision
        validation_function = validation.validate_project_metadata_xml_file
        resource_type = 'Project'
        resource_type_plural = 'Projects'
    if 'platform' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentPlatform
        resource_revision_mongodb_model = mongodb_models.PlatformRevision
        validation_function = validation.validate_platform_metadata_xml_file
        resource_type = 'Platform'
        resource_type_plural = 'Platforms'
    if 'instrument' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentInstrument
        resource_revision_mongodb_model = mongodb_models.InstrumentRevision
        validation_function = validation.validate_instrument_metadata_xml_file
        resource_type = 'Instrument'
        resource_type_plural = 'Instruments'
    if 'operation' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentOperation
        resource_revision_mongodb_model = mongodb_models.OperationRevision
        validation_function = validation.validate_operation_metadata_xml_file
        resource_type = 'Operation'
        resource_type_plural = 'Operations'
    if 'acquisition' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentAcquisition
        resource_revision_mongodb_model = mongodb_models.AcquisitionRevision
        validation_function = validation.validate_acquisition_metadata_xml_file
        conversion_validation_and_fixing_function = xml_conversion_checks_and_fixes.format_acquisition_dictionary
        resource_type = 'Acquisition'
        resource_type_plural = 'Acquisitions'
    if 'computation' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentComputation
        resource_revision_mongodb_model = mongodb_models.ComputationRevision
        validation_function = validation.validate_computation_metadata_xml_file
        conversion_validation_and_fixing_function = xml_conversion_checks_and_fixes.format_computation_dictionary
        resource_type = 'Computation'
        resource_type_plural = 'Computations'
    if 'process' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentProcess
        resource_revision_mongodb_model = mongodb_models.ProcessRevision
        validation_function = validation.validate_process_metadata_xml_file
        conversion_validation_and_fixing_function = xml_conversion_checks_and_fixes.format_process_dictionary
        resource_type = 'Process'
        resource_type_plural = 'Processes'
    if 'data-collection' in url_namespace:
        current_version_mongodb_model = mongodb_models.CurrentDataCollection
        resource_revision_mongodb_model = mongodb_models.DataCollectionRevision
        validation_function = validation.validate_data_collection_metadata_xml_file
        conversion_validation_and_fixing_function = xml_conversion_checks_and_fixes.format_data_collection_dictionary
        resource_type = 'Data Collection'
        resource_type_plural = 'Data Collections'
    return {
        'current_version_mongodb_model': current_version_mongodb_model,
        'resource_revision_mongodb_model': resource_revision_mongodb_model,
        'validation_function': validation_function,
        'conversion_validation_and_fixing_function': conversion_validation_and_fixing_function,
        'resource_type': resource_type,
        'resource_type_plural': resource_type_plural,
    }
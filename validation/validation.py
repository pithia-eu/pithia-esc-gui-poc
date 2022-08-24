import os
import traceback
import xmlschema
from requests import get
from lxml import etree
from rdflib import Graph, URIRef, RDF, SKOS
from search.ontology_helpers import ONTOLOGY_SERVER_BASE_URL
from validation.exceptions import InvalidRootElementNameForMetadataFileException, UnregisteredOntologyTermException, UnregisteredMetadataDocumentException
from common.mongodb_models import CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject

def validate_organisation_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Organisation')

def validate_individual_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Individual')

def validate_project_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Project')

def validate_platform_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Platform')

def validate_instrument_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Instrument')

def validate_operation_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Operation')

def validate_acquisition_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Acquisition')

def validate_computation_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Computation')

def validate_process_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Process')

def validate_data_collection_metadata_xml_file(self, xml_file):
    return _validate_metadata_xml_file(xml_file, 'Collection')

def parse_xml_file(xml_file):
    # Returns an ElementTree
    return etree.parse(xml_file)

def _create_validation_error_details_dict(err_type, err_message, extra_details):
    return {
        'type': str(err_type),
        'message': err_message,
        'extra_details': extra_details
    }

def _validate_metadata_xml_file(xml_file, expected_root_localname):
    validation_checklist = {
        'is_root_element_name_valid': False,
        'is_syntax_valid': False,
        'is_valid_against_schema': False,
        'is_each_document_reference_valid': False,
        'is_each_ontology_reference_valid': False,
    }

    try:
        # Syntax validation
        xml_file_parsed = etree.parse(xml_file)
        validation_checklist['is_syntax_valid'] = True

        # Root element name validation
        root_element_name_validation_details = validate_xml_root_element_name_equals_expected_name(xml_file_parsed, expected_root_localname)
        validation_checklist['is_root_element_name_valid'] = root_element_name_validation_details['is_root_element_name_valid']
        if not validation_checklist['is_root_element_name_valid']:
            validation_checklist['error'] = _create_validation_error_details_dict(InvalidRootElementNameForMetadataFileException, f"Expected the metadata file to have a root element name of \"{root_element_name_validation_details['expected_root_element_name']}\", but got \"{root_element_name_validation_details['root_element_name']}\".", None)
            return validation_checklist

        # XSD Schema validation
        parent = xml_file_parsed.getroot()
        urls_with_xsi_ns = parent.xpath("//@*[local-name()='schemaLocation' and namespace-uri()='http://www.w3.org/2001/XMLSchema-instance']")
        urls_with_xsi_ns = urls_with_xsi_ns[0].split()
        schema_url = urls_with_xsi_ns[0]
        if len(urls_with_xsi_ns) > 1:
            schema_url = urls_with_xsi_ns[1]
        validate_xml_against_schema_at_url(xml_file, schema_url)
        validation_checklist['is_valid_against_schema'] = True

        # Relation validaiton (whether a resource the metadata file
        # is referencing exists in the database or not).
        unregistered_references = get_unregistered_references_from_xml(xml_file_parsed)
        unregistered_document_hrefs = unregistered_references['document_hrefs']
        unregistered_document_types = unregistered_references['document_types']
        unregistered_ontology_term_hrefs = unregistered_references['ontology_term_hrefs']
        if len(unregistered_document_hrefs) > 0:
            validation_checklist['error'] = _create_validation_error_details_dict(type(UnregisteredMetadataDocumentException()), 'Unregistered document IRIs: %s.' % ', '.join(unregistered_document_hrefs), {
                'unregistered_document_types': unregistered_document_types
            })
            return validation_checklist
        validation_checklist['is_each_document_reference_valid'] = True
        if len(unregistered_ontology_term_hrefs) > 0:
            validation_checklist['error'] = _create_validation_error_details_dict(type(UnregisteredOntologyTermException()), 'Unregistered ontology term IRIs: %s.' % ', '.join(unregistered_ontology_term_hrefs), None)
            return validation_checklist
        validation_checklist['is_each_ontology_reference_valid'] = True
    except etree.XMLSyntaxError as err:
        print(traceback.format_exc())
        validation_checklist['error'] = _create_validation_error_details_dict(type(err), str(err), None)
    except etree.DocumentInvalid as err:
        print(traceback.format_exc())
        validation_checklist['error'] = _create_validation_error_details_dict(type(err), str(err), None)
    except BaseException as err:
        print(traceback.format_exc())
        validation_checklist['error'] = _create_validation_error_details_dict(type(err), str(err), None)
    

    return validation_checklist

def validate_xml_root_element_name_equals_expected_name(xml_file_parsed, expected_root_localname):
    root = xml_file_parsed.getroot()
    root_localname = etree.QName(root).localname # Get the root tag text without the namespace
    return {
        'root_element_name': f'{root_localname}',
        'expected_root_element_name': f'{expected_root_localname}',
        'is_root_element_name_valid': root_localname == expected_root_localname
    }

def validate_xml_against_schema_at_url(xml_file, schema_url):
    xml_file.seek(0)
    schema_response = get(schema_url)
    xml_schema = xmlschema.XMLSchema(schema_response.text.encode())
    xml_schema.validate(xml_file.read())

def validate_ontology_component_with_term(component, term_id):
    ontology_term_server_url = f'{ONTOLOGY_SERVER_BASE_URL}{component}/{term_id}'
    response = get(ontology_term_server_url) # e.g. http://ontology.espas-fp7.eu/relatedPartyRole/Operator
    if response.status_code == 404:
        return False
    if response.ok:
        response_text = response.text
        g = Graph()
        g.parse(data=response_text, format='application/rdf+xml')
        ontology_term = URIRef(ontology_term_server_url)
        return (ontology_term, RDF['type'], SKOS['Concept']) in g
    response.raise_for_status()
    return False

def get_mongodb_model_for_resource_type(resource_type):
    if resource_type == 'organisation':
        return CurrentOrganisation
    elif resource_type == 'individual':
        return CurrentIndividual
    elif resource_type == 'project':
        return CurrentProject
    elif resource_type == 'platform':
        return CurrentPlatform
    elif resource_type == 'operation':
        return CurrentOperation
    elif resource_type == 'instrument':
        return CurrentInstrument
    elif resource_type == 'acquisition':
        return CurrentAcquisition
    elif resource_type == 'computation':
        return CurrentComputation
    elif resource_type == 'process':
        return CurrentProcess
    elif resource_type == 'data-collection':
        return CurrentDataCollection
    return 'unknown'

def get_resource_from_xlink_href_components(resource_type, localID, namespace, version):
    find_dictionary = {
        'identifier.pithia:Identifier.localID': localID,
        'identifier.pithia:Identifier.namespace': namespace,
    }
    if version:
        find_dictionary['identifier.pithia:Identifier.version'] = version
    mongodb_model_for_resource_type = get_mongodb_model_for_resource_type(resource_type)
    return mongodb_model_for_resource_type.find_one(find_dictionary)

def get_components_from_xlink_href(href, href_section_to_remove):
    href = href.replace(href_section_to_remove, '')
    return href.split('/')

def get_unregistered_references_from_xml(xml_file_parsed):
    unregistered_references = {
        'document_hrefs': set(),
        'document_types': set(),
        'ontology_term_hrefs': set(),
    }
    parent = xml_file_parsed.getroot()
    hrefs = parent.xpath("//@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']")
    if not len(hrefs) > 0:
        for key in unregistered_references:
            unregistered_references[key] = list(unregistered_references[key])
        return unregistered_references
    for href in hrefs:
        if 'ontology' in href:
            href_components  = get_components_from_xlink_href(href, 'http://ontology.espas-fp7.eu/')
            ontology_component = href_components[0]
            ontology_term_id = href_components[1]
            is_valid_ontology_term = validate_ontology_component_with_term(ontology_component, ontology_term_id)
            if not is_valid_ontology_term:
                unregistered_references['ontology_term_hrefs'].add(href)

        if 'resources' in href:
            href_components  = get_components_from_xlink_href(href, 'http://resources.espas-fp7.eu/')
            resource_type = href_components[0]
            namespace = href_components[1]
            localID = href_components[2]
            version = None
            if len(href_components) > 3:
                version = href_components[3]
            referenced_resource = get_resource_from_xlink_href_components(resource_type, localID, namespace, version)
            if not referenced_resource:
                unregistered_references['document_hrefs'].add(href)
                unregistered_references['document_types'].add(resource_type)
    
    for key in unregistered_references:
        unregistered_references[key] = list(unregistered_references[key])
    return unregistered_references
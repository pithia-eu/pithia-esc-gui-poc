import re
import validators
from operator import itemgetter
from rdflib import (
    Graph,
    URIRef,
    RDF,
    SKOS,
)
from requests import get
from typing import List

from .file_wrappers import (
    AcquisitionCapabilitiesXMLMetadataFile,
    XMLMetadataFile,
)

from common.constants import PITHIA_METADATA_SERVER_HTTPS_URL_BASE
from common.models import (
    Instrument,
    ScientificMetadata,
)
from utils.url_helpers import (
    divide_resource_url_into_main_components,
    divide_resource_url_from_op_mode_id,
)


class MetadataFileOntologyURLReferencesValidator:
    @classmethod
    def _is_ontology_term_url_valid(cls, ontology_term_url: str):
        """Checks that the provided Space Physics Ontology URL
        has a valid HTTP response and that the response
        content is as expected.

        If the HTTP response code is 404 Not Found, the
        ontology term URL is treated as invalid.

        Any other HTTP response error code is treated
        as unexpected.
        """
        # e.g. https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/Operator/
        response = get(ontology_term_url)
        if response.status_code == 404:
            return False
        if response.ok:
            response_text = response.text
            g = Graph()
            g.parse(data=response_text, format='application/rdf+xml')
            ontology_term = URIRef(ontology_term_url)
            return (ontology_term, RDF['type'], SKOS['Concept']) in g
        response.raise_for_status()
        return False

    @classmethod
    def _is_each_ontology_url_valid(cls, ontology_urls: list):
        invalid_urls = []
        for url in ontology_urls:
            is_valid_ontology_term = cls._is_ontology_term_url_valid(url)
            if is_valid_ontology_term == False:
                invalid_urls.append(url)
        return invalid_urls
    
    @classmethod
    def is_each_ontology_url_in_xml_file_valid(cls, xml_file: XMLMetadataFile) -> List[str]:
        """Checks each Space Physics Ontology URL in the
        provided XML metadata file is valid.
        """
        ontology_urls = xml_file.ontology_urls
        return cls._is_each_ontology_url_valid(ontology_urls)
    
    @classmethod
    def is_each_potential_ontology_url_in_xml_file_valid(cls, xml_file: XMLMetadataFile) -> list[str]:
        """Checks each Space Physics Ontology URL in the
        provided XML metadata file is valid.
        """
        ontology_urls = xml_file.potential_ontology_urls
        return cls._is_each_ontology_url_valid(ontology_urls)


class MetadataFileMetadataURLReferencesValidator:
    # Keys to access invalid URL categories
    INCORRECTLY_STRUCTURED_URLS_KEY = 'urls_with_incorrect_structure'
    UNREGISTERED_RESOURCE_URLS_KEY = 'urls_pointing_to_unregistered_resources'
    UNREGISTERED_RESOURCE_URL_TYPES_KEY = 'types_of_missing_resources'

    @classmethod
    def _is_resource_url_well_formed(cls, resource_url):
        return validators.url(resource_url)
    
    @classmethod
    def _divide_resource_url_into_components(cls, resource_url):
        return divide_resource_url_into_main_components(resource_url)

    @classmethod
    def _is_resource_url_structure_valid(cls, resource_url):
        url_base, resource_type_in_resource_url, namespace, localid = itemgetter('url_base', 'resource_type', 'namespace', 'localid')(cls._divide_resource_url_into_components(resource_url))
        if any(
            component is None
            for component in [
                url_base,
                resource_type_in_resource_url,
                namespace,
                localid
            ]):
            return False

        # Verify resource type in resource URL is valid
        scientific_metadata_subclasses = ScientificMetadata.__subclasses__()
        is_resource_type_in_resource_url_valid = any(resource_type_in_resource_url == cls.type_in_metadata_server_url for cls in scientific_metadata_subclasses)

        # Verify that the localID base used in the resource
        # URL is valid (matches the resource type used in
        # the resource URL).
        localid_base = localid.split('_')[0]
        is_localid_base_valid = any(
            localid_base == cls.localid_base
            for cls in scientific_metadata_subclasses
        )
        is_resource_type_in_resource_url_matching_with_localid_base = any(
            (
                resource_type_in_resource_url == cls.type_in_metadata_server_url
                and localid_base == cls.localid_base
            )
            for cls in scientific_metadata_subclasses
        )

        return all([
            resource_url.startswith(PITHIA_METADATA_SERVER_HTTPS_URL_BASE),
            resource_url.count(PITHIA_METADATA_SERVER_HTTPS_URL_BASE) == 1,
            is_resource_type_in_resource_url_valid,
            is_localid_base_valid,
            is_resource_type_in_resource_url_matching_with_localid_base,
            url_base == PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
            len(re.findall(f'(?=/{resource_type_in_resource_url}/)', resource_url)) == 1,
            len(re.findall(f'(?=/{namespace}/)', resource_url)) == 1,
            len(re.findall(f'(?=/{localid})', resource_url)) == 1,
            resource_url.endswith(localid),
        ])

    @classmethod
    def _is_resource_url_valid(cls, resource_url):
        validation_summary_for_metadata_server_url = {
            'is_structure_valid': False,
            'is_pointing_to_registered_resource': False,
            'type_of_missing_resource': None,
        }
        if not cls._is_resource_url_well_formed(resource_url):
            return validation_summary_for_metadata_server_url
        
        if not cls._is_resource_url_structure_valid(resource_url):
            return validation_summary_for_metadata_server_url
        validation_summary_for_metadata_server_url['is_structure_valid'] = True

        try:
            ScientificMetadata.objects.get_by_metadata_server_url(resource_url)
        except ScientificMetadata.DoesNotExist:
            resource_type_in_resource_url, localid = itemgetter('resource_type', 'localid')(cls._divide_resource_url_into_components(resource_url))
            validation_summary_for_metadata_server_url['type_of_missing_resource'] = resource_type_in_resource_url
            if resource_type_in_resource_url == 'staticDataset':
                validation_summary_for_metadata_server_url['type_of_missing_resource'] = ('staticDataset', localid)
            return validation_summary_for_metadata_server_url
        validation_summary_for_metadata_server_url['is_pointing_to_registered_resource'] = True

        return validation_summary_for_metadata_server_url

    @classmethod
    def _is_each_resource_url_valid(cls, resource_urls: List[str]) -> dict:
        """Checks that each metadata server URL is well-formed and that each URL
        corresponds with a metadata registration in the e-Science Centre.
        """
        incorrectly_structured_urls = list()
        unregistered_resource_urls = list()
        unregistered_resource_url_types = list()

        # Find if there is a issue with each resource URL submitted,
        # then sort into categories.
        for resource_url in resource_urls:
            is_structure_valid, is_pointing_to_registered_resource, type_of_missing_resource = itemgetter(
                'is_structure_valid',
                'is_pointing_to_registered_resource',
                'type_of_missing_resource'
            )(cls._is_resource_url_valid(resource_url))
            if not is_structure_valid:
                incorrectly_structured_urls.append(
                    resource_url
                )
            elif not is_pointing_to_registered_resource:
                unregistered_resource_urls.append(resource_url)
                unregistered_resource_url_types.append(type_of_missing_resource)

        # Remove duplicate URLs/URL types and return results
        return {
            cls.INCORRECTLY_STRUCTURED_URLS_KEY: incorrectly_structured_urls,
            cls.UNREGISTERED_RESOURCE_URLS_KEY: unregistered_resource_urls,
            cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY: unregistered_resource_url_types,
        }

    @classmethod
    def is_each_resource_url_valid(cls, xml_file: XMLMetadataFile) -> dict:
        """Checks that each metadata server URL is valid by
        meeting a specified set of criteria.
        """
        resource_urls = xml_file.metadata_urls
        return cls._is_each_resource_url_valid(resource_urls)

    @classmethod
    def is_each_potential_resource_url_valid(cls, xml_file: XMLMetadataFile) -> dict:
        """Checks that each potential metadata server URL is valid by
        meeting a specified set of criteria.
        """
        resource_urls = xml_file.potential_metadata_urls
        return cls._is_each_resource_url_valid(resource_urls)

    @classmethod
    def _process_validation_results(cls, unprocessed_validation_results) -> dict:
        # Remove duplicates and combine invalid URLs with
        # invalid URLs derived from operational mode URLs.
        incorrectly_structured_urls = unprocessed_validation_results.get(cls.INCORRECTLY_STRUCTURED_URLS_KEY, [])
        unregistered_resource_urls = unprocessed_validation_results.get(cls.UNREGISTERED_RESOURCE_URLS_KEY, [])
        
        # Return results depending on what problem occurred.
        results = dict()
        # Incorrectly structured URLs
        if len(incorrectly_structured_urls) > 0:
            results.update({
                'incorrectly_structured_urls': list(set(incorrectly_structured_urls)),
            })

        # Unregistered resource URLs
        if len(unregistered_resource_urls) > 0:
            results.update({
                'unregistered_resource_urls': list(set(unregistered_resource_urls)),
                'types_in_unregistered_resource_urls': list(set(unprocessed_validation_results.get(cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY, []))),
            })

        return results

    @classmethod
    def validate_and_return_results(cls, xml_metadata_file: XMLMetadataFile) -> dict:
        # Check which resource URLs are valid and return
        # the invalid ones.
        unprocessed_validation_results = cls.is_each_potential_resource_url_valid(xml_metadata_file)
        results = cls._process_validation_results(unprocessed_validation_results)

        # Invalid ontology URLs
        invalid_ontology_urls = MetadataFileOntologyURLReferencesValidator.is_each_potential_ontology_url_in_xml_file_valid(xml_metadata_file)
        if len(invalid_ontology_urls) > 0:
            results.update({
                'invalid_ontology_urls': invalid_ontology_urls,
            })

        return results


class AcquisitionCapabilitiesMetadataFileMetadataURLReferencesValidator(MetadataFileMetadataURLReferencesValidator):
    UNREGISTERED_OPERATIONAL_MODE_URLS_KEY = 'urls_pointing_to_registered_resources_with_missing_op_modes'
    INSTRUMENTS_TO_UPDATE_KEY = 'instruments_to_update'

    @classmethod
    def is_each_potential_operational_mode_url_valid(cls, xml_file: AcquisitionCapabilitiesXMLMetadataFile) -> dict:
        """Checks that each potential operational mode URL is well-formed
        and that each URL corresponds with a metadata registration in the
        e-Science Centre.
        """
        # Check file is for Acquisition Capabilities.
        try:
            resource_urls_with_op_mode_ids = xml_file.potential_operational_mode_urls
        except:
            # Only Acquisition Capabilities XML files
            # have potential operational mode URLs.
            return cls._is_each_resource_url_valid([])

        # Check if instruments referenced in operational
        # mode URLs are registered.
        op_mode_urls_without_op_mode_ids = [
            itemgetter('resource_url')(divide_resource_url_from_op_mode_id(url))
            for url in resource_urls_with_op_mode_ids
        ]
        resource_url_validation_results = cls._is_each_resource_url_valid(op_mode_urls_without_op_mode_ids)

        # Find unregistered operational modes of registered
        # instruments, and add any operational mode URLs failing
        # other checks.
        unprocessed_op_mode_url_validation_results = {
            cls.INCORRECTLY_STRUCTURED_URLS_KEY: list(),
            cls.UNREGISTERED_RESOURCE_URLS_KEY: list(),
            cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY: list(),
        }
        unregistered_operational_mode_urls = list()
        instruments_with_unregistered_operational_modes = list()
        for url in resource_urls_with_op_mode_ids:
            resource_url = itemgetter('resource_url')(divide_resource_url_from_op_mode_id(url))
            # Incorrect structure check
            if resource_url in resource_url_validation_results.get(
                cls.INCORRECTLY_STRUCTURED_URLS_KEY, []):
                unprocessed_op_mode_url_validation_results[cls.INCORRECTLY_STRUCTURED_URLS_KEY].append(
                    url
                )
                continue
            # Check resource is registered in eSC
            type_from_resource_url = itemgetter('resource_type')(cls._divide_resource_url_into_components(resource_url))
            try:
                instrument = Instrument.objects.get_by_metadata_server_url(resource_url)
            except Exception:
                unprocessed_op_mode_url_validation_results[cls.UNREGISTERED_RESOURCE_URLS_KEY].append(url)
                unprocessed_op_mode_url_validation_results[cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY].append(
                    type_from_resource_url
                )
                continue
            # Check operational mode is registered
            try:
                Instrument.objects.get_by_operational_mode_url(url)
            except Exception:
                unregistered_operational_mode_urls.append(url)
                instruments_with_unregistered_operational_modes.append(instrument)

        unprocessed_op_mode_url_validation_results.update({
            cls.UNREGISTERED_OPERATIONAL_MODE_URLS_KEY: unregistered_operational_mode_urls,
            cls.INSTRUMENTS_TO_UPDATE_KEY: instruments_with_unregistered_operational_modes,
        })
        
        return unprocessed_op_mode_url_validation_results

    @classmethod
    def _process_validation_results(cls, unprocessed_validation_results) -> dict:
        results = super()._process_validation_results(unprocessed_validation_results)

        # Unregistered operational mode URLs
        unregistered_operational_mode_urls = unprocessed_validation_results.get(cls.UNREGISTERED_OPERATIONAL_MODE_URLS_KEY, [])
        if len(unregistered_operational_mode_urls) > 0:
            results.update({
                'unregistered_operational_mode_urls': list(set(unregistered_operational_mode_urls)),
                'instruments_to_update': unprocessed_validation_results.get(cls.INSTRUMENTS_TO_UPDATE_KEY, []),
            })

        return results

    @classmethod
    def validate_and_return_results(cls, xml_metadata_file: AcquisitionCapabilitiesXMLMetadataFile) -> dict:
        results = super().validate_and_return_results(xml_metadata_file)
        # Check which operational mode URLs are valid and return
        # the invalid ones.
        unprocessed_operational_mode_url_validation_results = cls.is_each_potential_operational_mode_url_valid(xml_metadata_file)
        results = results | cls._process_validation_results(unprocessed_operational_mode_url_validation_results)

        return results
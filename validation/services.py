import logging
import os
import xmlschema
from datetime import (
    datetime,
    timezone,
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape
from typing import Union
from xmlschema.exceptions import XMLSchemaException

from .errors import (
    FileRegisteredBefore,
    UpdateFileNotMatching,
)
from .file_wrappers import (
    InstrumentXMLMetadataFile,
    XMLMetadataFile,
)
from .helpers import (
    map_acquisition_capability_to_update_link,
    map_string_to_li_element,
)

from common.models import (
    Instrument,
    AcquisitionCapabilities,
    ScientificMetadata,
)
from pithiaesc.settings import BASE_DIR

logger = logging.getLogger(__name__)


class MetadataFileXSDValidator:
    @classmethod
    def _instantiate_pithia_schema(cls):
        try:
            cwd_before_validation = os.getcwd()
            # Temporarily change the cwd to so the XSD
            # validator can see the schema files.
            os.chdir(os.path.join(BASE_DIR, 'validation', 'local_schema_files'))
            with open(os.path.join('pithia.xsd')) as schema_file:
                schema = xmlschema.XMLSchema(schema_file)
        finally:
            # Change the cwd back as XSD validation is
            # finished.
            os.chdir(cwd_before_validation)
        
        return schema

    @classmethod
    def _validate_xml_file_string_against_schema(cls, xml_file_string: str, schema: xmlschema.XMLSchema):
        schema.validate(xml_file_string)

    @classmethod
    def validate(cls, xml_file: XMLMetadataFile):
        """Validates an XML metadata file against the schema it
        specifies at its schemaLocation URL.
        """
        schema = cls._instantiate_pithia_schema()
        return cls._validate_xml_file_string_against_schema(xml_file.contents, schema)

    @classmethod
    def validate_and_return_errors(cls, xml_metadata_file: XMLMetadataFile):
        errors = []
        try:
            cls.validate(xml_metadata_file)
        except XMLSchemaException as err:
            logger.exception('Error occurred during metadata validation.')
            error_msg = f'<span style="white-space: pre-wrap;">{escape(str(err).strip())}</span>'
            errors.append(error_msg)
        return errors


class MetadataFileRegistrationValidator:
    @classmethod
    def _is_localid_already_in_use(cls, localid: str, model: ScientificMetadata = ScientificMetadata):
        try:
            model.objects.get(pk=localid)
        except ObjectDoesNotExist:
            return False
        return True

    @classmethod
    def check_if_localid_is_already_in_use_and_return_suggestion_if_taken(cls, localid: str):
        result = MetadataFileRegistrationValidator._is_localid_already_in_use(localid)
        result_dict = {
            'result': result,
        }
        if result:
            result_dict['suggestion'] = f'{localid}{int(datetime.now(timezone.utc).timestamp())}'
        return result_dict

    @classmethod
    def validate(cls, xml_file: XMLMetadataFile, model: ScientificMetadata):
        """Validates whether an XML metadata file has been
        registered before or not.
        """
        xml_file_localid = xml_file.localid
        if not cls._is_localid_already_in_use(xml_file_localid, model):
            return False
        
        raise FileRegisteredBefore(
            f'Metadata sharing the same localID of "{xml_file_localid}" has already been registered with the e-Science Centre.',
        )

    @classmethod
    def validate_and_return_errors(cls, xml_metadata_file: XMLMetadataFile, model: ScientificMetadata):
        errors = []
        try:
            cls.validate(xml_metadata_file, model)
        except FileRegisteredBefore as err:
            logger.exception('Error occurred during metadata validation.')
            error_msg = str(err)
            errors.append(error_msg)
        return errors


class MetadataFileUpdateValidator:
    @classmethod
    def validate(cls, xml_file: XMLMetadataFile, model: ScientificMetadata, metadata_registration_id: str):
        """Validates whether the localID and namespace of
        an updated XML metadata file matches the localID
        and namespace of its current corresponding
        e-Science Centre registration.
        """
        xml_file_localid = xml_file.localid
        xml_file_namespace = xml_file.namespace
        existing_registration = model.objects.get(pk=metadata_registration_id)
        if (not xml_file_localid == existing_registration.localid
            or not xml_file_namespace == existing_registration.namespace):
            raise UpdateFileNotMatching('The localID and namespace must be matching with the current version of the metadata.')

    @classmethod
    def validate_and_return_errors(cls, xml_metadata_file: XMLMetadataFile, model: ScientificMetadata, existing_metadata_id: str):
        errors = []
        try:
            cls.validate(xml_metadata_file, model, existing_metadata_id)
        except UpdateFileNotMatching as err:
            logger.exception('Error occurred during metadata validation.')
            error_msg = str(err)
            errors.append(error_msg)
        except ObjectDoesNotExist:
            logger.exception('Error occurred during metadata validation.')
            error_msg = 'The metadata registration being updated could not be found.'
            errors.append(error_msg)
        return errors


class InstrumentMetadataFileValidator:
    @classmethod
    def is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
        self,
        xml_file: InstrumentXMLMetadataFile,
        current_instrument_id,
        model: Instrument
    ) -> Union[bool, list]:
        """Checks whether each Operational Mode ID present in
        the Instrument that is currently registered is also
        within the updated XML metadata file for that
        Instrument.
        """
        operational_mode_ids_of_updated_xml = xml_file.operational_mode_ids
        instrument_to_update = model.objects.get(pk=current_instrument_id)
        operational_mode_ids_of_current_xml = instrument_to_update.operational_mode_ids
        operational_mode_ids_intersection = set(operational_mode_ids_of_updated_xml).intersection(set(operational_mode_ids_of_current_xml))
        result = len(operational_mode_ids_intersection) == len(operational_mode_ids_of_current_xml)
        missing_ids = [id for id in list(operational_mode_ids_of_current_xml) if id not in list(operational_mode_ids_intersection)]
        missing_operational_mode_urls = [f'{instrument_to_update.metadata_server_url}#{id}' for id in missing_ids]
        return result, missing_operational_mode_urls

    @classmethod
    def validate_and_return_errors(cls, xml_metadata_file: InstrumentXMLMetadataFile, existing_metadata_id: str):
        errors = []
        try:
            # Operational mode IDs are changed and pre-existing IDs are referenced by any Acquisition Capabilities validation
            is_each_op_mode_in_update_valid, missing_operational_mode_urls = cls.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
                xml_metadata_file,
                existing_metadata_id,
                Instrument
            )
            if not is_each_op_mode_in_update_valid:
                acquisition_capability_sets = AcquisitionCapabilities.objects.referencing_operational_mode_urls(missing_operational_mode_urls)
                if len(acquisition_capability_sets) == 0:
                    return errors
                error_msg = '<div class="mt-2">Any references to the following operational modes will be invalidated after this update:<div>'
                error_msg = error_msg + '<ul class="mt-3">%s</ul>' % ''.join(list(map(map_string_to_li_element, missing_operational_mode_urls)))
                error_msg = error_msg + '<div class="mt-3">To fix this, please also update any references to this instrument\'s operational mode IDs in the acquisition capabilities listed below, after updating this instrument:</div><ul class="mt-3">%s</ul>' % ''.join(list(map(map_acquisition_capability_to_update_link, acquisition_capability_sets)))
                errors.append(error_msg)
        except AttributeError:
            logger.exception('This metadata file doesn\'t have operational modes')
        return errors
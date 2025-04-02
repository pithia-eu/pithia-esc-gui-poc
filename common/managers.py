import json
import os
import uuid
import xmltodict
from django.apps import apps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from lxml import etree
from typing import Union

from .helpers import clean_localid_or_namespace


class ScientificMetadataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('json__name')

    def _parse_xml_file_or_string(self, xml_file_or_string):
        xml_string = xml_file_or_string
        
        # For SimpleUploadedFile objects
        if hasattr(xml_string, 'read'):
            xml_string.seek(0)
            xml_string = xml_string.read()
        
        # For bytes-like objects
        try:
            xml_string = xml_string.decode()
        except (UnicodeDecodeError, AttributeError):
            pass

        return etree.fromstring(xml_string.encode('utf-8'))

    def _convert_xml_metadata_file_to_dictionary(self, xml_file_or_string: Union[InMemoryUploadedFile, str]) -> dict:
        xml = xml_file_or_string
        if hasattr(xml_file_or_string, 'read'):
            xml_file_or_string.seek(0)
            xml = xml_file_or_string.read()
        xml_as_dict = xmltodict.parse(xml)
        xml_as_json = json.dumps(xml_as_dict)
        # Some formatting to get rid of '\n' characters and extra
        # whitespace within strings
        xml_as_json = xml_as_json.replace('\\n', '')
        xml_as_json = ' '.join(xml_as_json.split())
        # Convert JSON back to a dictionary so it's easier to
        # work with.
        return json.loads(xml_as_json)

    def _format_metadata_file_xml_for_db(self, metadata_file_xml):
        metadata_file_dict = self._convert_xml_metadata_file_to_dictionary(metadata_file_xml)
        # Remove the top-level tag - this will be just <Organisation>, for example
        metadata_file_dict = metadata_file_dict[(list(metadata_file_dict)[0])]
        return metadata_file_dict

    def _clean_localid_and_namespace_in_xml_string(self, xml_string):
        parsed_xml = self._parse_xml_file_or_string(xml_string)
        local_id_element = parsed_xml.find('.//{https://metadata.pithia.eu/schemas/2.2}localID')
        local_id_element.text = clean_localid_or_namespace(local_id_element.text)
        namespace_element = parsed_xml.find('.//{https://metadata.pithia.eu/schemas/2.2}namespace')
        namespace_element.text = clean_localid_or_namespace(namespace_element.text)
        return etree.tostring(parsed_xml)
    
    def _create_from_xml_string(
        self,
        xml_string: str,
        type: str,
        institution_id: str,
        owner_id: str
    ):
        cleaned_xml_string = self._clean_localid_and_namespace_in_xml_string(xml_string)

        try:
            cleaned_xml_string = cleaned_xml_string.decode()
        except (UnicodeDecodeError, AttributeError):
            pass

        xml_as_dict = self._format_metadata_file_xml_for_db(cleaned_xml_string)

        scientific_metadata = self.using(os.environ['DJANGO_RW_DATABASE_NAME']).create(
            id=xml_as_dict['identifier']['PITHIA_Identifier']['localID'],
            type=type,
            xml=cleaned_xml_string,
            json=xml_as_dict,
            institution_id=institution_id,
            owner_id=owner_id
        )

        return scientific_metadata


    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        pass


    def update_from_xml_string(self, pk, xml_string: str, owner_id: str):
        cleaned_xml_string = self._clean_localid_and_namespace_in_xml_string(xml_string)

        try:
            cleaned_xml_string = cleaned_xml_string.decode()
        except (UnicodeDecodeError, AttributeError):
            pass

        xml_as_dict = self._format_metadata_file_xml_for_db(cleaned_xml_string)

        registration = self.get(pk=pk)
        registration.xml = cleaned_xml_string
        registration.json = xml_as_dict
        registration.owner_id = owner_id
        registration.save(using=os.environ['DJANGO_RW_DATABASE_NAME'])
        return registration
    
    class Meta:
        abstract = True

class OrganisationManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.ORGANISATION)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.ORGANISATION, institution_id, owner_id)

class IndividualManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.INDIVIDUAL)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.INDIVIDUAL, institution_id, owner_id)

class ProjectManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.PROJECT)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.PROJECT, institution_id, owner_id)

class PlatformManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.PLATFORM)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.PLATFORM, institution_id, owner_id)

class OperationManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.OPERATION)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.OPERATION, institution_id, owner_id)

class InstrumentManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.INSTRUMENT)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.INSTRUMENT, institution_id, owner_id)

class AcquisitionCapabilitiesManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.ACQUISITION_CAPABILITIES)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.ACQUISITION_CAPABILITIES, institution_id, owner_id)

class AcquisitionManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.ACQUISITION)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.ACQUISITION, institution_id, owner_id)

class ComputationCapabilitiesManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.COMPUTATION_CAPABILITIES)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.COMPUTATION_CAPABILITIES, institution_id, owner_id)

class ComputationManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.COMPUTATION)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.COMPUTATION, institution_id, owner_id)

class ProcessManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.PROCESS)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.PROCESS, institution_id, owner_id)

class DataCollectionManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.DATA_COLLECTION)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.DATA_COLLECTION, institution_id, owner_id)

class StaticDatasetManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.CATALOGUE)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.CATALOGUE, institution_id, owner_id)

class StaticDatasetEntryManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.CATALOGUE_ENTRY)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.CATALOGUE_ENTRY, institution_id, owner_id)

class DataSubsetManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.CATALOGUE_DATA_SUBSET)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.CATALOGUE_DATA_SUBSET, institution_id, owner_id)

class WorkflowManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.WORKFLOW)

    def create_from_xml_string(self, xml_string: str, institution_id: str, owner_id: str):
        return super()._create_from_xml_string(xml_string, self.model.WORKFLOW, institution_id, owner_id)
    
class InteractionMethodManager(models.Manager):
    pass

class APIInteractionMethodManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(scientific_metadata__type=apps.get_model('common', 'ScientificMetadata').DATA_COLLECTION, type=self.model.API)

    def create_api_interaction_method(self, specification_url: str, description: str, data_collection):
        config = {
            'specification_url': specification_url,
            'description': description,
        }
        interaction_method = self.model(
            id=uuid.uuid4(),
            type=self.model.API,
            scientific_metadata=data_collection,
            config=config,
            owner=0
        )
        interaction_method.save(using=os.environ['DJANGO_RW_DATABASE_NAME'])

        return interaction_method

    def update_config(self, interaction_method_id, specification_url: str, description: str = ''):
        interaction_method = self.get_queryset().get(pk=interaction_method_id)
        interaction_method.specification_url = specification_url
        interaction_method.description = description
        interaction_method.save(using=os.environ['DJANGO_RW_DATABASE_NAME'])
        return interaction_method
    
class WorkflowAPIInteractionMethodManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(scientific_metadata__type=apps.get_model('common', 'ScientificMetadata').WORKFLOW, type=self.model.API)
    
    def create_api_interaction_method(self, specification_url: str, description: str, workflow):
        config = {
            'specification_url': specification_url,
            'description': description,
        }
        interaction_method = self.model(
            id=uuid.uuid4(),
            type=self.model.API,
            scientific_metadata=workflow,
            config=config,
            owner=0
        )
        interaction_method.save(using=os.environ['DJANGO_RW_DATABASE_NAME'])

        return interaction_method

    def update_config(self, interaction_method_id, specification_url: str, description: str = ''):
        interaction_method = self.get_queryset().get(pk=interaction_method_id)
        interaction_method.specification_url = specification_url
        interaction_method.description = description
        interaction_method.save(using=os.environ['DJANGO_RW_DATABASE_NAME'])
        return interaction_method
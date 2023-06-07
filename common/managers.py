import json
import xmltodict
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models import Q
from typing import Union


class ScientificMetadataManager(models.Manager):
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
        # pymongo takes dictionaries when inserting new documents,
        # so convert the JSON back to a dictionary
        return json.loads(xml_as_json)

    def _format_metadata_file_xml_for_db(self, metadata_file_xml):
        metadata_file_dict = self._convert_xml_metadata_file_to_dictionary(metadata_file_xml)
        # Remove the top-level tag - this will be just <Organisation>, for example
        metadata_file_dict = metadata_file_dict[(list(metadata_file_dict)[0])]
        return metadata_file_dict
    
    def _create_from_xml_string(self, xml_string: str, resource_type: str):
        xml_as_dict = self._format_metadata_file_xml_for_db(xml_string)
        
        try:
            xml_string = xml_string.decode()
        except (UnicodeDecodeError, AttributeError):
            pass

        scientific_metadata = self.model(
            resource_type=resource_type,
            xml=xml_string,
            json=xml_as_dict,
        )
        scientific_metadata.id = scientific_metadata.localid
        scientific_metadata.save()

        return scientific_metadata


    def create_from_xml_string(self, xml_string: str):
        pass

    def update_from_xml_string(self, pk, xml_string: str):
        xml_as_dict = self._format_metadata_file_xml_for_db(xml_string)

        try:
            xml_string = xml_string.decode()
        except (UnicodeDecodeError, AttributeError):
            pass

        registration = self.get(pk=pk)
        registration.xml = xml_string
        registration.json = xml_as_dict
        return registration.save()
    
    class Meta:
        abstract = True

class OrganisationManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.ORGANISATION)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.ORGANISATION)

class IndividualManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.INDIVIDUAL)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.INDIVIDUAL)

class ProjectManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.PROJECT)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.PROJECT)

class PlatformManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.PLATFORM)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.PLATFORM)

class OperationManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.OPERATION)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.OPERATION)

class InstrumentManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.INSTRUMENT)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.INSTRUMENT)

class AcquisitionCapabilitiesManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.ACQUISITION_CAPABILITIES)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.ACQUISITION_CAPABILITIES)

class AcquisitionManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.ACQUISITION)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.ACQUISITION)

class ComputationCapabilitiesManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.COMPUTATION_CAPABILITIES)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.COMPUTATION_CAPABILITIES)

class ComputationManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.COMPUTATION)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.COMPUTATION)

class ProcessManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.PROCESS)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.PROCESS)

class DataCollectionManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.DATA_COLLECTION)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.DATA_COLLECTION)

class CatalogueManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.CATALOGUE)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.CATALOGUE)

class CatalogueEntryManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.CATALOGUE_ENTRY)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.CATALOGUE_ENTRY)

class CatalogueDataSubsetManager(ScientificMetadataManager):
    def get_queryset(self):
        return super().get_queryset().filter(resource_type=self.model.CATALOGUE_DATA_SUBSET)

    def create_from_xml_string(self, xml_string: str):
        return super()._create_from_xml_string(xml_string, self.model.CATALOGUE_DATA_SUBSET)
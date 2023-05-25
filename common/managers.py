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
    
    def get_by_namespace_and_localid(self, namespace: str, localid: str):
        return self.get(
            json__identifier__PITHIA_Identifier__namespace=namespace,
            json_metadata__identifier__PITHIA_Identifier__localID=localid
        )

    def with_localids(self, localids: list):
        return self.get_queryset().filter(
            json__identifier__PITHIA_Identifier__localID__in=localids
        )
    
    def create_from_xml_string(self, xml_string: str, resource_type: str):
        xml_as_dict = self._format_metadata_file_xml_for_db(xml_string)
        
        try:
            xml_string = xml_string.decode()
        except (UnicodeDecodeError, AttributeError):
            pass

        metadata_registration = self.create(
            resource_type=resource_type,
            xml=xml_string,
            json=xml_as_dict,
        )

        return metadata_registration

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
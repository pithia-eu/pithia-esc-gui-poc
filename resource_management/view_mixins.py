from django.utils.text import slugify

from common.xml_metadata_mapping_shortcuts import CatalogueDataSubsetXmlMappingShortcuts


class CatalogueDataSubsetResourceManagementViewMixin:
    SIMILAR_SOURCE_NAMES_ERROR = 'Some online resource names in the metadata file are too similar to one another. Please update the metadata file to resolve these issues, then re-upload it.'
    
    def check_source_names(self, form):
        self.temp_xml_file = self.request.FILES.getlist('files')[0]
        data_subset_shortcutted = CatalogueDataSubsetXmlMappingShortcuts(self.temp_xml_file.read().decode())
        source_names = [
            source.get('name', '')
            for source in data_subset_shortcutted.online_resources
            if source.get('name', '')
        ]
        source_names_normalised = set(
            slugify(source_name)
            for source_name in source_names
        )
        return len(source_names) == len(source_names_normalised)
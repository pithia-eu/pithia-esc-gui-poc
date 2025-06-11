import dateutil.parser
import json
import logging
from lxml import etree

from metadata_editor.xml_ns_enums import Namespace, NamespacePrefix


logger = logging.getLogger(__name__)


class EditorFormFieldsToMetadataUtilsMixin:
    xml_string_parsed = None
    DEFAULT_XPATH_NSPREFIX = 'PITHIA'
    basic_form_field_to_xml_mappings = {}

    def __init__(self, xml_string) -> None:
        self.xml_string = xml_string
        self.xml_string_parsed = etree.fromstring(xml_string.encode('utf-8'))
        self.namespaces = {
            NamespacePrefix.GCO: Namespace.GCO,
            NamespacePrefix.GMD: Namespace.GMD,
            NamespacePrefix.GML: Namespace.GML,
            NamespacePrefix.MRL: Namespace.MRL,
            NamespacePrefix.OM: Namespace.OM,
            self.DEFAULT_XPATH_NSPREFIX: Namespace.PITHIA,
            NamespacePrefix.XLINK: Namespace.XLINK,
            NamespacePrefix.XSI: Namespace.XSI,
        }

    def _get_first_element_from_list(self, element_list: list):
        return next(iter(element_list), '')

    def _get_element_text_or_blank_string(self, element):
        try:
            return element.text
        except AttributeError:
            pass
        return ''

    def get_basic_form_field_to_xml_field_mappings(self):
        return {}

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        return {}

    def get_initial_values_with_basic_mappings(self):
        basic_mappings = self.get_basic_form_field_to_xml_field_mappings()
        initial_values_from_basic_mappings = {}
        for field_name, query in basic_mappings.items():
            elements_matching_query = self.xml_string_parsed.xpath(query, namespaces=self.namespaces)
            if not elements_matching_query:
                continue
            try:
                initial_values_from_basic_mappings[field_name] = self._get_first_element_from_list(elements_matching_query).text
            except AttributeError as err:
                initial_values_from_basic_mappings[field_name] = self._get_first_element_from_list(elements_matching_query)
            except BaseException as err:
                logger.exception(err)
                continue
        return initial_values_from_basic_mappings

    def get_initial_values_from_basic_multiple_choice_mappings(self):
        basic_mc_mappings = self.get_basic_multiple_choice_form_field_to_xml_field_mappings()
        initial_values_from_basic_mc_mappings = {}
        for field_name, query in basic_mc_mappings.items():
            elements_matching_query = self.xml_string_parsed.xpath(query, namespaces=self.namespaces)
            if not elements_matching_query:
                continue
            try:
                initial_values_from_basic_mc_mappings[field_name] = [e.text for e in elements_matching_query if e.text]
            except AttributeError as err:
                initial_values_from_basic_mc_mappings[field_name] = elements_matching_query
            except BaseException as err:
                logger.exception(err)
                continue
        return initial_values_from_basic_mc_mappings

    def get_initial_values_with_custom_mappings(self):
        return {}

    def get_initial_form_values(self):
        initial_values = {}
        initial_values_from_basic_mappings = self.get_initial_values_with_basic_mappings()
        initial_values_from_multiple_choice_mappings = self.get_initial_values_from_basic_multiple_choice_mappings()
        initial_values_from_custom_mappings = self.get_initial_values_with_custom_mappings()
        initial_values.update(initial_values_from_basic_mappings)
        initial_values.update(initial_values_from_multiple_choice_mappings)
        initial_values.update(initial_values_from_custom_mappings)
        return initial_values


class BaseMetadataFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'localid': './/%s:localID' % self.DEFAULT_XPATH_NSPREFIX,
            'namespace': './/%s:namespace' % self.DEFAULT_XPATH_NSPREFIX,
            'name': './/%s:name' % self.DEFAULT_XPATH_NSPREFIX,
            'description': './/%s:description' % self.DEFAULT_XPATH_NSPREFIX,
            'identifier_version': './/%s:version' % self.DEFAULT_XPATH_NSPREFIX,
        })
        return mappings


class CapabilitiesFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def _map_process_capabilities_to_form(self):
        process_capability_elements = self.xml_string_parsed.xpath('.//%s:capabilities/%s:processCapability' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX), namespaces=self.namespaces)
        process_capabilities = []
        for e in process_capability_elements:
            name_elements = e.xpath('.//%s:name' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
            name = ''
            try:
                name = self._get_element_text_or_blank_string(self._get_first_element_from_list(name_elements))
            except AttributeError:
                pass
            observed_property_elements = e.xpath('.//%s:observedProperty/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            observed_property = self._get_first_element_from_list(observed_property_elements)
            dimensionality_instance_elements = e.xpath('.//%s:dimensionalityInstance/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            dimensionality_instance = self._get_first_element_from_list(dimensionality_instance_elements)
            dimensionality_timeline_elements = e.xpath('.//%s:dimensionalityTimeline/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            dimensionality_timeline = self._get_first_element_from_list(dimensionality_timeline_elements)
            cadence_elements = e.xpath('.//%s:cadence' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
            cadence = ''
            try:
                cadence = self._get_element_text_or_blank_string(self._get_first_element_from_list(cadence_elements))
            except AttributeError:
                pass
            cadence_unit_attributes = e.xpath('.//%s:cadence/@unit' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
            cadence_unit = self._get_first_element_from_list(cadence_unit_attributes)
            vector_representations = e.xpath('.//%s:vectorRepresentation/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            coordinate_system_elements = e.xpath('.//%s:coordinateSystem/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            coordinate_system = self._get_first_element_from_list(coordinate_system_elements)
            units_elements = e.xpath('.//%s:units/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            units = self._get_first_element_from_list(units_elements)
            qualifiers = e.xpath('.//%s:qualifier/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            process_capabilities.append({
                'name': name,
                'observedProperty': observed_property,
                'dimensionalityInstance': dimensionality_instance,
                'dimensionalityTimeline': dimensionality_timeline,
                'cadence': cadence,
                'cadenceUnits': cadence_unit,
                'vectorRepresentation': vector_representations,
                'coordinateSystem': coordinate_system,
                'units': units,
                'qualifier': qualifiers,
            })
        return process_capabilities

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        capabilities = self._map_process_capabilities_to_form()
        initial_values.update({
            'capabilities_json': capabilities
        })
        return initial_values


class StandardIdentifierFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def _map_standard_identifiers_to_form(self, parent_element):
        standard_identifier_elements = parent_element.xpath('.//%s:standardIdentifier' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
        standard_identifiers = []
        for e in standard_identifier_elements:
            value = self._get_element_text_or_blank_string(e)
            standard_identifiers.append({
                'authority': e.get('authority', ''),
                'value': value,
            })
        return standard_identifiers


class CapabilityLinkFormFieldsToMetadataMixin(
    StandardIdentifierFormFieldsToMetadataMixin,
    EditorFormFieldsToMetadataUtilsMixin):
    def _map_time_spans_to_form(self, parent_element):
        time_span_elements = parent_element.xpath('.//%s:timeSpan' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
        time_spans = []
        for time_span_elem in time_span_elements:
            begin_positions = time_span_elem.xpath('.//%s:beginPosition' % NamespacePrefix.GML, namespaces=self.namespaces)
            begin_position = self._get_element_text_or_blank_string(self._get_first_element_from_list(begin_positions))
            end_positions = time_span_elem.xpath('.//%s:endPosition/@indeterminatePosition' % NamespacePrefix.GML, namespaces=self.namespaces)
            end_position = self._get_first_element_from_list(end_positions)
            time_spans.append({
                'beginPosition': begin_position,
                'endPosition': end_position,
            })
        return time_spans

    def _map_capability_links_to_form(self):
        capability_link_elements = self.xml_string_parsed.xpath('.//%s:capabilityLink' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
        capability_links = []
        for cap_link_elem in capability_link_elements:
            platforms = cap_link_elem.xpath('.//%s:platform/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            capabilities = cap_link_elem.xpath('.//%s:%s/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, self.capabilities_element_key, NamespacePrefix.XLINK), namespaces=self.namespaces)
            standard_identifiers = self._map_standard_identifiers_to_form(cap_link_elem)
            time_spans = self._map_time_spans_to_form(cap_link_elem)
            capability_links.append({
                'platforms': platforms,
                'capabilities': capabilities,
                'standardIdentifiers': json.dumps(standard_identifiers),
                'timeSpans': json.dumps(time_spans),
            })
        return capability_links
    
    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        capability_links = self._map_capability_links_to_form()
        initial_values.update({'capability_links_json': capability_links})
        return initial_values


class ContactInfoFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'phone': './/%s:voice/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'delivery_point': './/%s:deliveryPoint/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'city': './/%s:city/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'administrative_area': './/%s:administrativeArea/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'postal_code': './/%s:postalCode/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'country': './/%s:country/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'email_address': './/%s:electronicMailAddress/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'online_resource': './/%s:linkage/%s:URL' % (NamespacePrefix.GMD, NamespacePrefix.GMD),
            'contact_instructions': './/%s:contactInstructions/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
        })
        return mappings

    def _get_hours_of_service_from_xml(self):
        hours_of_service_elements = self.xml_string_parsed.xpath('.//%s:hoursOfService/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO), namespaces=self.namespaces)
        if not hours_of_service_elements:
            return {}
        
        hours_of_service_element = self._get_first_element_from_list(hours_of_service_elements)
        try:
            hours_of_service_split = hours_of_service_element.text.split('-')
        except AttributeError as err:
            logger.exception(err)
            return {}

        hours_of_service = {}
        try:
            hours_of_service_start = hours_of_service_split[0]
            hours_of_service['hours_of_service_start'] = dateutil.parser.parse(hours_of_service_start).time().strftime('%H:%M')
        except IndexError as err:
            logger.exception(err)
        
        try:
            hours_of_service_end = hours_of_service_split[1]
            hours_of_service['hours_of_service_end'] = dateutil.parser.parse(hours_of_service_end).time().strftime('%H:%M')
        except IndexError as err:
            logger.exception(err)

        return hours_of_service

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()

        try:
            hours_of_service = self._get_hours_of_service_from_xml()
            initial_values.update(hours_of_service)
        except BaseException as err:
            logger.exception(err)

        return initial_values


class DataLevelFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'data_levels': './/%s:dataLevel/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings


class DocumentationFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'citation_title': './/%s:documentation/%s:Citation/%s:title/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_publication_date': './/%s:documentation/%s:Citation/%s:date/%s:CI_Date/%s:date/%s:Date' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_doi': './/%s:documentation/%s:Citation/%s:identifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_linkage_url': './/%s:documentation/%s:Citation/%s:onlineResource/%s:CI_OnlineResource/%s:linkage/%s:URL' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD),
            'other_citation_details': './/%s:documentation/%s:Citation/%s:otherCitationDetails/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GCO),
        })
        return mappings

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        documentation_citations = []
        documentation_citation_elements = self.xml_string_parsed.xpath('.//%s:documentation/%s:Citation' % (
            self.DEFAULT_XPATH_NSPREFIX,
            self.DEFAULT_XPATH_NSPREFIX
        ), namespaces=self.namespaces)
        for element in documentation_citation_elements:
            titles = element.xpath('.//%s:title/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO), namespaces=self.namespaces)
            publication_dates = element.xpath('.//%s:date/%s:CI_Date/%s:date/%s:Date' % (NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO), namespaces=self.namespaces)
            dois = element.xpath('.//%s:identifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO), namespaces=self.namespaces)
            other_citation_details = element.xpath('.//%s:otherCitationDetails/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO), namespaces=self.namespaces)
            linkage_urls = element.xpath('.//%s:onlineResource/%s:CI_OnlineResource/%s:linkage/%s:URL' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD), namespaces=self.namespaces)
            documentation_citations.append({
                'title': self._get_element_text_or_blank_string(self._get_first_element_from_list(titles)),
                'publicationDate': self._get_element_text_or_blank_string(self._get_first_element_from_list(publication_dates)),
                'doi': self._get_element_text_or_blank_string(self._get_first_element_from_list(dois)),
                'otherCitationDetails': self._get_element_text_or_blank_string(self._get_first_element_from_list(other_citation_details)),
                'linkageUrl': self._get_element_text_or_blank_string(self._get_first_element_from_list(linkage_urls)),
            })
        initial_values.update({
            'citations_json': documentation_citations,
        })
        return initial_values


class InputOutputFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def _map_input_outputs_to_form(self, input_outputs_container_element_name):
        input_outputs = []
        input_outputs_container_elements = self.xml_string_parsed.xpath('.//%s:%s/%s:InputOutput' % (self.DEFAULT_XPATH_NSPREFIX, input_outputs_container_element_name, self.DEFAULT_XPATH_NSPREFIX), namespaces=self.namespaces)
        for e in input_outputs_container_elements:
            name = self._get_element_text_or_blank_string(
                self._get_first_element_from_list(
                    e.xpath('.//%s:name' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
                )
            )
            description = self._get_element_text_or_blank_string(
                self._get_first_element_from_list(
                    e.xpath('.//%s:description/%s:LE_Source/%s:description/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.MRL, NamespacePrefix.MRL, self.GCO19115_NSPREFIX), namespaces=self.namespaces)
                )
            )
            input_outputs.append({
                'name': name,
                'description': description,
            })
        return input_outputs


class LocationFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self._nested_location_element_xpath = '%s:location/%s:Location' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX)
        self._geometry_location_element_xpath = '%s:geometryLocation' % (self.DEFAULT_XPATH_NSPREFIX)

    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'location_name': './/%s/%s:nameLocation/%s:EX_GeographicDescription/%s:geographicIdentifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self._nested_location_element_xpath, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'geometry_location_point_id': './/%s/%s/%s:Point/@%s:id' % (self._nested_location_element_xpath, self._geometry_location_element_xpath, NamespacePrefix.GML, NamespacePrefix.GML),
            'geometry_location_point_srs_name': './/%s/%s/%s:Point/@srsName' % (self._nested_location_element_xpath, self._geometry_location_element_xpath, NamespacePrefix.GML),
        })
        return mappings

    def _get_geometry_location_pos_data_from_xml(self):
        geometry_location_point_pos_elements = self.xml_string_parsed.xpath(
            './/%s/%s/%s:Point/%s:pos' % (self._nested_location_element_xpath, self._geometry_location_element_xpath, NamespacePrefix.GML, NamespacePrefix.GML),
            namespaces=self.namespaces
        )
        if not geometry_location_point_pos_elements:
            return {}

        geometry_location_point_pos_element = self._get_first_element_from_list(geometry_location_point_pos_elements)
        try:
            pos_text = geometry_location_point_pos_element.text
            pos_text_split = pos_text.split()
        except AttributeError as err:
            logger.exception(err)
            return {}

        pos_data = {}
        try:
            pos_data['geometry_location_point_pos_1'] = pos_text_split[0]
        except IndexError as err:
            logger.exception(err)

        try:
            pos_data['geometry_location_point_pos_2'] = pos_text_split[1]
        except IndexError as err:
            logger.exception(err)
        
        return pos_data
    
    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()

        gl_point_pos_data = self._get_geometry_location_pos_data_from_xml()
        initial_values.update(gl_point_pos_data)

        return initial_values


class QualityAssessmentFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'data_quality_flags': './/%s:qualityAssessment/%s:dataQualityFlag/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'metadata_quality_flags': './/%s:qualityAssessment/%s:metadataQualityFlag/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings


class RelatedPartyFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        initial_values['related_parties_json'] = []
        responsible_party_info_elements = self.xml_string_parsed.xpath('.//%s:ResponsiblePartyInfo' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
        for rpi in responsible_party_info_elements:
            roles = rpi.xpath('.//%s:role/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            parties = rpi.xpath('.//%s:party/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            initial_values['related_parties_json'].append({
                'role': self._get_first_element_from_list(roles),
                'parties': parties,
            })
        return initial_values


class SourceFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def _map_source_to_form(self, online_resource_element):
        service_functions = online_resource_element.xpath('.//%s:serviceFunction/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
        linkages = online_resource_element.xpath('.//%s:linkage/%s:URL' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD), namespaces=self.namespaces)
        linkage = self._get_element_text_or_blank_string(self._get_first_element_from_list(linkages))
        names = online_resource_element.xpath('.//%s:name' % (self.DEFAULT_XPATH_NSPREFIX), namespaces=self.namespaces)
        name = self._get_element_text_or_blank_string(self._get_first_element_from_list(names))
        protocols = online_resource_element.xpath('.//%s:protocol' % (self.DEFAULT_XPATH_NSPREFIX), namespaces=self.namespaces)
        protocol = self._get_element_text_or_blank_string(self._get_first_element_from_list(protocols))
        descriptions = online_resource_element.xpath('.//%s:description' % (self.DEFAULT_XPATH_NSPREFIX), namespaces=self.namespaces)
        description = self._get_element_text_or_blank_string(self._get_first_element_from_list(descriptions))
        data_formats = online_resource_element.xpath('.//%s:dataFormat/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
        return {
            'serviceFunctions': service_functions,
            'linkage': linkage,
            'name': name,
            'protocol': protocol,
            'description': description,
            'dataFormats': data_formats,
        }
    
    def _map_sources_to_form(self, online_resource_elements_xpath: str = None):
        sources = []
        online_resource_elements = self.xml_string_parsed.xpath(online_resource_elements_xpath, namespaces=self.namespaces)
        for e in online_resource_elements:
            source = self._map_source_to_form(e)
            sources.append(source)
        return sources

    def get_initial_values_with_custom_mappings(self):
        mappings = super().get_initial_values_with_custom_mappings()
        mappings.update({
            'sources_json': self._map_sources_to_form()
        })
        return mappings


class BaseTimePeriodFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self._gml_id_xpath_section = '@%s:id' % NamespacePrefix.GML
        self._time_instant_element_xpath_section = '%s:TimeInstant' % NamespacePrefix.GML
        self._time_position_element_xpath_section = '%s:timePosition' % NamespacePrefix.GML
        self._time_period_element_xpath_section = '%s:%s/%s:TimePeriod' % (self.DEFAULT_XPATH_NSPREFIX, self.time_period_container_element_name, NamespacePrefix.GML)


class MultipleTimePeriodFormFieldsToMetadataMixin(BaseTimePeriodFormFieldsToMetadataMixin):
    def _map_time_period_to_form(self, time_period_element):
        time_period_begin_position = self._get_element_text_or_blank_string(self._get_first_element_from_list(time_period_element.xpath('.//%s:begin/%s/%s' % (NamespacePrefix.GML, self._time_instant_element_xpath_section, self._time_position_element_xpath_section), namespaces=self.namespaces)))
        if time_period_begin_position:
            time_period_begin_position = dateutil.parser.parse(time_period_begin_position).replace(second=0, microsecond=0).isoformat().replace('+00:00', '')
        time_period_end_position = self._get_element_text_or_blank_string(self._get_first_element_from_list(time_period_element.xpath('.//%s:end/%s/%s' % (NamespacePrefix.GML, self._time_instant_element_xpath_section, self._time_position_element_xpath_section), namespaces=self.namespaces)))
        if time_period_end_position:
            time_period_end_position = dateutil.parser.parse(time_period_end_position).replace(second=0, microsecond=0).isoformat().replace('+00:00', '')
        return {
            'timeInstantBeginPosition': time_period_begin_position,
            'timeInstantEndPosition': time_period_end_position,
        }

    def _map_time_periods_to_form(self):
        time_periods = []
        time_period_elements = self.xml_string_parsed.xpath(
            './/%s' % self._time_period_element_xpath_section,
            namespaces=self.namespaces
        )
        for e in time_period_elements:
            time_period = self._map_time_period_to_form(e)
            time_periods.append(time_period)
        return time_periods


class TimePeriodFormFieldsToMetadataMixin(BaseTimePeriodFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'time_instant_begin_position': './/%s/%s:begin/%s/%s' % (self._time_period_element_xpath_section, NamespacePrefix.GML, self._time_instant_element_xpath_section, self._time_position_element_xpath_section),
            'time_instant_end_position': './/%s/%s:end/%s/%s' % (self._time_period_element_xpath_section, NamespacePrefix.GML, self._time_instant_element_xpath_section, self._time_position_element_xpath_section),
        })
        return mappings


class TypeFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'type': './/%s:type/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK)
        })
        return mappings
import os

from django.db import models
from django.db.models import Q
from operator import itemgetter

from utils.url_helpers import (
    divide_resource_url_from_op_mode_id,
    get_namespace_and_localid_from_resource_url,
)


class ScientificMetadataQuerySet(models.QuerySet):
    def get_by_namespace_and_localid(self, namespace: str, localid: str):
        """A metadata registration using the passed in
        namespace and localID.
        """
        return self.get(
            json__identifier__PITHIA_Identifier__namespace=namespace,
            json__identifier__PITHIA_Identifier__localID=localid
        )

    def get_by_metadata_server_url(self, metadata_server_url: str):
        """A metadata registration corresponding to the
        metadata server URL passed in.
        """
        try:
            localid = metadata_server_url.split('/')[-1]
        except Exception:
            raise self.model.DoesNotExist
        return self.get(pk=localid)
    
    def get_by_metadata_server_urls(self, metadata_server_urls: list):
        """Metadata registrations corresponding to at least
        one of the URLs from a list of metadata server URLs.
        """
        if not metadata_server_urls:
            return self.none()
        query = Q()
        for url in metadata_server_urls:
            localid = url.split('/')[-1]
            query |= Q(pk=localid)
        return self.filter(query)

    def delete_by_metadata_server_urls(self, metadata_server_urls: list):
        """Deletes all metadata registrations corresponding to
        at least one of the URLs in a list of metadata
        server URLs.
        """
        if not metadata_server_urls:
            return
        localids = [get_namespace_and_localid_from_resource_url(url)[1] for url in metadata_server_urls]
        registrations_for_deletion = list(self.filter(
            json__identifier__PITHIA_Identifier__localID__in=localids
        ))
        for r in registrations_for_deletion:
            r.delete(using=os.environ['DJANGO_RW_DATABASE_NAME'])

    def owned_by_institution(self, institution_id: str):
        return self.filter(institution_id=institution_id)


class OrganisationQuerySet(ScientificMetadataQuerySet):
    def for_simple_search(self, query_sections: list):
        """Organisations with a name containing all of the
        passed in query sections.
        """
        search_query = Q()
        for qs in query_sections:
            search_query &= Q(json__name__icontains=qs)
        return self.filter(search_query)


class IndividualQuerySet(ScientificMetadataQuerySet):
    def referencing_organisation_url(self, organisation_url: str):
        """Individuals referencing a given Organisation URL.
        """
        return self.filter(**{'json__organisation__@xlink:href': organisation_url})

    def for_delete_chain(self, metadata_server_url: str):
        """Individuals referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        referencing_organisation_url = self.referencing_organisation_url(metadata_server_url)
        return referencing_organisation_url


class ProjectQuerySet(ScientificMetadataQuerySet):
    def referencing_party_url(self, party_url: str):
        """Projects referencing a given Organisation
        or Individual URL.
        """
        return self.filter(**{'json__relatedParty__contains': [{'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}]})

    def for_delete_chain(self, metadata_server_url: str):
        """Projects referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        return referencing_party_url

    def for_simple_search(self, query_sections: list):
        """Projects with a name containing all of the
        passed in query sections.
        """
        search_query = Q()
        for qs in query_sections:
            search_query &= Q(json__name__icontains=qs)
        return self.filter(search_query)


class PlatformQuerySet(ScientificMetadataQuerySet):
    def referencing_party_url(self, party_url: str):
        """Platforms referencing a given Organisation
        or Individual URL.
        """
        return self.filter(**{
            'json__relatedParty__contains': [
                {'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}
            ]
        })
    
    def referencing_platform_url(self, platform_url: str):
        """Platforms referencing a given Platform URL.
        """
        return self.filter(**{
            'json__childPlatform__contains': [{'@xlink:href': platform_url}]
        })

    def for_delete_chain(self, metadata_server_url: str):
        """Platforms referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        referencing_other_platforms = self.referencing_platform_url(metadata_server_url)
        return referencing_party_url | referencing_other_platforms


class OperationQuerySet(ScientificMetadataQuerySet):
    def referencing_party_url(self, party_url: str):
        """Operations referencing a given Organisation
        or Individual URL.
        """
        return self.filter(**{
            'json__relatedParty__contains': [
                {'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}
            ]
        })
    
    def referencing_platform_url(self, platform_url: str):
        """Operations referencing a given Platform URL.
        """
        return self.filter(**{
            'json__platform__contains': [{'@xlink:href': platform_url}]
        })

    def for_delete_chain(self, metadata_server_url: str):
        """Operations referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        referencing_platform_url = self.referencing_platform_url(metadata_server_url)
        return referencing_party_url | referencing_platform_url


class InstrumentQuerySet(ScientificMetadataQuerySet):
    def distinct_instrument_type_urls(self):
        """All distinct Instrument Type URLs among all
        registered Instruments.
        """
        return self.values_list('json__type__@xlink:href', flat=True).distinct()

    def get_by_operational_mode_url(self, operational_mode_url: str):
        metadata_server_url, op_mode_id = itemgetter(
            'resource_url', 'op_mode_id'
        )(divide_resource_url_from_op_mode_id(operational_mode_url))
        namespace, localid = get_namespace_and_localid_from_resource_url(metadata_server_url)
        return self.get(
            json__identifier__PITHIA_Identifier__namespace=namespace,
            json__identifier__PITHIA_Identifier__localID=localid,
            json__operationalMode__contains=[{'InstrumentOperationalMode': {'id': op_mode_id}}]
        )
    
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        """Instruments referencing at least one URL from
        a list of Instrument Type URLs.
        """
        if not instrument_type_urls:
            return self.none()
        query = Q()
        for url in instrument_type_urls:
            query |= Q(**{'json__type__@xlink:href__contains': url})
        return self.filter(query)
    
    def referencing_party_url(self, party_url: str):
        """Instruments referencing a given Organisation
        or Individual URL.
        """
        return self.filter(**{
            'json__relatedParty__contains': [
                {'ResponsiblePartyInfo': {'party': {'@xlink:href': party_url}}}
            ]
        })

    def for_search_by_instrument_type_urls(self, instrument_type_urls: list):
        return self.referencing_instrument_type_urls(instrument_type_urls)
    
    def for_search(self, instrument_type_urls: list):
        """Instruments referencing at least one URL
        from a list of Instrument Type URLs.
        """
        return self.referencing_instrument_type_urls(instrument_type_urls)

    def for_delete_chain(self, metadata_server_url: str):
        """Instruments referencing a URL corresponding to a metadata
        registration that is planned for deletion.
        """
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        return referencing_party_url


class AcquisitionCapabilitiesQuerySet(ScientificMetadataQuerySet):
    def referencing_instrument_url(self, instrument_url: str):
        """Acquisition Capabilities registrations referencing a given
        Instrument URL.
        """
        return self.filter(**{
            'json__instrumentModePair__InstrumentOperationalModePair__instrument__@xlink:href': instrument_url
        })

    def referencing_instrument_urls(self, instrument_urls: list):
        """Acquisition Capabilities referencing at least one URL from
        a list of Instrument URLs.
        """
        if not instrument_urls:
            return self.none()
        query = Q()
        for url in instrument_urls:
            query |= Q(**{
                'json__instrumentModePair__InstrumentOperationalModePair__instrument__@xlink:href': url
            })
        return self.filter(query)

    def referencing_observed_property_urls(self, observed_property_urls: list):
        """Acquisition Capabilities referencing at least one URL from
        a list of Observed Property URLs.
        """
        if not observed_property_urls:
            return self.none()
        query = Q()
        for url in observed_property_urls:
            query |= Q(**{
                'json__capabilities__processCapability__contains': [
                    {'observedProperty': {'@xlink:href': url}}
                ]
            })
        return self.filter(query)
    
    def referencing_operational_mode_urls(self, operational_mode_urls: list):
        """Acquisition Capabilities referencing at least one URL from
        a list of operational mode URLs.
        """
        if not operational_mode_urls:
            return self.none()
        query = Q()
        for url in operational_mode_urls:
            query |= Q(**{
                'json__instrumentModePair__InstrumentOperationalModePair__mode__@xlink:href': url
            })
        return self.filter(query)

    def for_search_by_instrument_type_urls(self, instrument_urls: list):
        return self.referencing_instrument_urls(instrument_urls)

    def for_search_by_observed_property_urls(self, observed_property_urls: list):
        return self.referencing_observed_property_urls(observed_property_urls)

    def for_search(self, instrument_urls: list, observed_property_urls: list):
        """Acquisition Capabilities matching both of the following criteria:
        * Referencing at least one URL from a list of
          Instrument URLs.
        * Referencing at least one URL from a list of
          Observed Property URLs.

        If one list is empty, only the non-empty list for its
        corresponding condition must be true.
        """
        results_referencing_instrument_urls = self.referencing_instrument_urls(
            instrument_urls
        )
        results_referencing_observed_property_urls = self.referencing_observed_property_urls(
            observed_property_urls
        )
        
        # If none are found to be referencing Instrument
        # URLs, just return those that are referencing
        # Observed Property URLs.
        if not instrument_urls:
            return results_referencing_observed_property_urls
        
        # If none are found to be referencing Observed
        # Property URLs, just return those that are
        # referencing Instrument URLs.
        if not observed_property_urls:
            return results_referencing_instrument_urls

        return results_referencing_instrument_urls & results_referencing_observed_property_urls
    
    def for_delete_chain(self, metadata_server_url: str, operational_mode_urls: list = []):
        """Acquisition Capabilities referencing a URL
        corresponding to a metadata registration
        that is planned for deletion.
        """
        referencing_instrument_url = self.referencing_instrument_url(metadata_server_url)
        referencing_operational_mode_urls = self.referencing_operational_mode_urls(
            operational_mode_urls
        )
        return referencing_instrument_url | referencing_operational_mode_urls


class AcquisitionQuerySet(ScientificMetadataQuerySet):
    def referencing_acquisition_capability_set_url(self, acquisition_capability_set_url: str):
        """Acquisitions referencing a given Acquisition Capabilities URL.
        """
        return self.filter(**{
            'json__capabilityLinks__capabilityLink__contains': [
                {'acquisitionCapabilities': {'@xlink:href': acquisition_capability_set_url}}
            ]
        })

    def referencing_acquisition_capability_set_urls(self, acquisition_capability_set_urls: list):
        """Acquisitions referencing at least one URL from a list of Acquisition Capabilities.
        """
        if not acquisition_capability_set_urls:
            return self.none()
        query = Q()
        for url in acquisition_capability_set_urls:
            query |= Q(**{
                'json__capabilityLinks__capabilityLink__contains': [
                    {'acquisitionCapabilities': {'@xlink:href': url}}
                ]
            })
        return self.filter(query)
    
    def referencing_instrument_url(self, instrument_url: str):
        """Acquisitions referencing a given Instrument URL.
        """
        return self.filter(**{'json__instrument__@xlink:href': instrument_url})

    def referencing_platform_url(self, platform_url: str):
        """Acquisitions referencing a given Platform URL.
        """
        return self.filter(**{
            'json__capabilityLinks__capabilityLink__contains': [
                {'platform': {'@xlink:href': platform_url}}
            ]
        })

    def for_search_by_instrument_type_urls(self, acquisition_capability_set_urls: list):
        return self.referencing_acquisition_capability_set_urls(acquisition_capability_set_urls)

    def for_search_by_observed_property_urls(self, acquisition_capability_set_urls: list):
        return self.referencing_acquisition_capability_set_urls(acquisition_capability_set_urls)

    def for_search(self, acquisition_capability_set_urls: list):
        """Acquisitions referencing at least one URL from a
        list of Acquisition Capabilities URLs.
        """
        return self.referencing_acquisition_capability_set_urls(acquisition_capability_set_urls)
    
    def for_delete_chain(self, metadata_server_url: str):
        """Acquisitions referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        referencing_instrument_url = self.referencing_instrument_url(metadata_server_url)
        referencing_acquisition_capability_set_url = self.referencing_acquisition_capability_set_url(
            metadata_server_url
        )
        referencing_platform_url = self.referencing_platform_url(metadata_server_url)
        return (referencing_instrument_url
                | referencing_acquisition_capability_set_url
                | referencing_platform_url)


class ComputationCapabilitiesQuerySet(ScientificMetadataQuerySet):
    def referencing_computation_type_urls(self, computation_type_urls: list):
        """Computation Capabilities referencing at least one URL from a
        list of Computation Type URLs.
        """
        if not computation_type_urls:
            return self.none()
        query = Q()
        for url in computation_type_urls:
            query |= Q(**{'json__type__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def referencing_observed_property_urls(self, observed_property_urls: list):
        """Computation Capabilities referencing at least one URL from a
        list of Observed Property URLs.
        """
        if not observed_property_urls:
            return self.none()
        query = Q()
        for url in observed_property_urls:
            query |= Q(**{
                'json__capabilities__processCapability__contains': [
                    {'observedProperty': {'@xlink:href': url}}
                ]
            })
        return self.filter(query)
    
    def referencing_computation_capability_set_url(self, computation_capability_set_url: str):
        """Computation Capabilities referencing the passed in
        Computation Capabilities URL.
        """
        return self.filter(json__childComputation__contains=[
            {'@xlink:href': computation_capability_set_url}
        ])
    
    def _immediate_computation_capability_set_referers(self, computation_capability_set):
        """Computation Capabilities registrations referencing a given
        Computation Capabilities registration.
        """
        return self.referencing_computation_capability_set_url(
            computation_capability_set.metadata_server_url
        )
    
    def all_computation_capability_set_referers(self, computation_capability_set, initial_referers_list=[]):
        """Computation Capabilities registrations referencing the passed
        in Computation Capabilities registration, in addition to
        recursively performing the same process on each referer.
        """
        all_referers = initial_referers_list
        immediate_referers = list(
            self._immediate_computation_capability_set_referers(computation_capability_set)
        )
        for ir in immediate_referers:
            if not any(
                str(ir.pk) == str(r.pk)
                for r in all_referers
            ):
                all_referers.append(ir)
                all_referers += self.all_computation_capability_set_referers(ir)
        return list({
            str(r.pk): r
            for r in all_referers
        }.values())
    
    def _immediate_child_computations(self, computation_capability_set):
        """Child Computation Capabilities registrations of a given Computation Capabilities
        registration.
        """
        child_computation_urls = [
            child_computation['@xlink:href']
            for child_computation in computation_capability_set.json['childComputation']
        ]
        return self.get_by_metadata_server_urls(child_computation_urls)
    
    def all_child_computations(self, computation_capability_set, initial_child_computation_list=[]):
        """Child computation Capabilities registrations referencing the passed
        in Computation Capabilities registration, in addition to
        recursively performing the same process on each child Computation
        Capabilities registration.
        """
        all_child_computations = initial_child_computation_list
        immediate_child_computations = list(
            self._immediate_child_computations(computation_capability_set)
        )
        for icc in immediate_child_computations:
            if not any(
                icc.pk == cc.pk
                for cc in all_child_computations
            ):
                all_child_computations.append(icc)
                self.all_child_computations(icc, all_child_computations)
        return all_child_computations

    def _merge_computation_capability_set_referers_for_search(self, computation_capability_sets: list):
        # Find the Computation Capabilities referencing to the found
        # registrations.
        related_computation_capability_sets = []
        for cc in computation_capability_sets:
            related_computation_capability_sets += self.all_computation_capability_set_referers(
                cc,
                initial_referers_list=[]
            )
        
        # Merge all results into a list of primary keys
        merged_list = computation_capability_sets + related_computation_capability_sets
        merged_list = list(set(cc.pk for cc in merged_list))

        # Convert everything back to QuerySets
        return self.filter(pk__in=merged_list)

    def for_search_by_computation_type_urls(self, computation_type_urls: list):
        computation_capability_sets = self.referencing_computation_type_urls(computation_type_urls)
        return self._merge_computation_capability_set_referers_for_search(list(computation_capability_sets))

    def for_search_by_observed_property_urls(self, observed_property_urls: list):
        computation_capability_sets = self.referencing_observed_property_urls(observed_property_urls)
        return self._merge_computation_capability_set_referers_for_search(list(computation_capability_sets))

    def for_search(self, computation_type_urls: list, observed_property_urls: list):
        """Computation Capabilities matching both of the following criteria:
        * Referencing at least one URL from a list
          of Computation Type URLs.
        * Referencing at least one URL from a list
          of Observed Property URLs.

        If one list is empty, only the non-empty list for its
        corresponding condition must be true.
        """
        # Find Computation Capabilities registrations by Computation Types
        # and Observed Properties
        results_referencing_computation_type_urls = self.referencing_computation_type_urls(
            computation_type_urls
        )
        results_referencing_observed_property_urls = self.referencing_observed_property_urls(
            observed_property_urls
        )
        referencing_available_urls = []
        if computation_type_urls and observed_property_urls:
            referencing_available_urls = list(
                results_referencing_computation_type_urls \
                & results_referencing_observed_property_urls
            )
        elif computation_type_urls:
            referencing_available_urls = list(results_referencing_computation_type_urls)
        elif observed_property_urls:
            referencing_available_urls = list(results_referencing_observed_property_urls)

        # Find the Computation Capabilities referencing to the found
        # registrations.
        related_computation_capability_sets = []
        for cc in referencing_available_urls:
            related_computation_capability_sets += self.all_computation_capability_set_referers(
                cc,
                initial_referers_list=[]
            )

        # Merge all results into a list of primary keys
        merged_list = referencing_available_urls + related_computation_capability_sets
        merged_list = list(set(cc.pk for cc in merged_list))

        # Convert everything back to QuerySets
        return self.filter(pk__in=merged_list)
    
    def for_delete_chain(self, metadata_server_url: str):
        """Computation Capabilities referencing a URL corresponding to a
        metadata registration that is planned for deletion.
        """
        referencing_computation_capability_set_url = self.referencing_computation_capability_set_url(
            metadata_server_url
        )
        return referencing_computation_capability_set_url


class ComputationQuerySet(ScientificMetadataQuerySet):
    def referencing_computation_capability_set_url(self, computation_capability_set_url: str):
        """Computations referencing a given Computation Capabilities URL.
        """
        return self.filter(**{
            'json__capabilityLinks__capabilityLink__contains': [
                {'computationCapabilities': {'@xlink:href': computation_capability_set_url}}
            ]
        })

    def referencing_computation_capability_set_urls(self, computation_capability_set_urls: list):
        """Computations referencing at least one URL from a list
        of Computation Capabilities by URL in the passed in list.
        """
        if not computation_capability_set_urls:
            return self.none()
        query = Q()
        for url in computation_capability_set_urls:
            query |= Q(**{
                'json__capabilityLinks__capabilityLink__contains': [
                    {'computationCapabilities': {'@xlink:href': url}}
                ]
            })
        return self.filter(query)

    def for_search_by_computation_type_urls(self, computation_capability_set_urls: list):
        return self.referencing_computation_capability_set_urls(
            computation_capability_set_urls
        )

    def for_search_by_observed_property_urls(self, computation_capability_set_urls: list):
        return self.referencing_computation_capability_set_urls(
            computation_capability_set_urls
        )

    def for_search(self, computation_capability_set_urls: list):
        """Computations referencing at least one URL from a list
        of Computation Capabilities URLs.
        """
        return self.referencing_computation_capability_set_urls(
            computation_capability_set_urls
        )
    
    def for_delete_chain(self, metadata_server_url: str):
        """Computations referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        referencing_computation_capability_set_url = self.referencing_computation_capability_set_url(
            metadata_server_url
        )
        return referencing_computation_capability_set_url


class ProcessQuerySet(ScientificMetadataQuerySet):
    def referencing_acquisition_url(self, acquisition_url: str):
        """Processes referencing a given Acquisition URL.
        """
        return self.filter(**{
            'json__acquisitionComponent__contains': [
                {'@xlink:href': acquisition_url}
            ]
        })

    def referencing_acquisition_urls(self, acquisition_urls: list):
        """Processes referencing at least one URL from a list
        of Acquisition URLs.
        """
        if not acquisition_urls:
            return self.none()
        query = Q()
        for url in acquisition_urls:
            query |= Q(**{
                'json__acquisitionComponent__contains': [
                    {'@xlink:href': url}
                ]
            })
        return self.filter(query)
    
    def referencing_computation_url(self, computation_url: str):
        """Processes referencing a given Computation URL.
        """
        return self.filter(**{
            'json__computationComponent__contains': [
                {'@xlink:href': computation_url}
            ]
        })

    def referencing_computation_urls(self, computation_urls: list):
        """Processes referencing at least one URL from a list
        of Computation URLs.
        """
        if not computation_urls:
            return self.none()
        query = Q()
        for url in computation_urls:
            query |= Q(**{
                'json__computationComponent__contains': [
                    {'@xlink:href': url}
                ]
            })
        return self.filter(query)

    def referencing_observed_property_urls(self, observed_property_urls: list):
        if not observed_property_urls:
            return self.none()
        query = Q()
        for url in observed_property_urls:
            query |= Q(**{
                'json__capabilities__processCapability__contains': [
                    {'observedProperty': {'@xlink:href': url}}
                ]
            })
            query |= Q(**{
                'json__capabilities__processCapability__observedProperty__@xlink:href': url
            })
        return self.filter(query)

    def for_search_by_instrument_type_urls(self, acquisition_urls: list):
        return self.referencing_acquisition_urls(acquisition_urls)

    def for_search_by_computation_type_urls(self, computation_urls: list):
        return self.referencing_computation_urls(computation_urls)

    def for_search_by_observed_property_urls(self, acquisition_urls: list, computation_urls: list, observed_property_urls: list):
        return self.referencing_acquisition_urls(acquisition_urls) \
            | self.referencing_computation_urls(computation_urls) \
            | self.referencing_observed_property_urls(observed_property_urls)

    def for_search(self, acquisition_urls: list, computation_urls: list):
        """Processes meeting at least one of the following criteria:
        * Referencing at least one URL from a list of Acquisition URLs
        * Referencing at least one URL from a list of Computation URLs
        """
        return self.referencing_acquisition_urls(acquisition_urls) \
            | self.referencing_computation_urls(computation_urls)
    
    def for_delete_chain(self, metadata_server_url: str):
        """Processes referencing a URL corresponding
        to a metadata registration that is planned
        for deletion.
        """
        referencing_acquisition_url = self.referencing_acquisition_url(metadata_server_url)
        referencing_computation_url = self.referencing_computation_url(metadata_server_url)
        return referencing_acquisition_url | referencing_computation_url


class DataCollectionQuerySet(ScientificMetadataQuerySet):
    def referencing_feature_of_interest_urls(self, feature_of_interest_urls: list):
        """Data Collections referencing at least one URL
        from a list of Feature of Interest URLs.
        """
        if not feature_of_interest_urls:
            return self.none()
        query = Q()
        for url in feature_of_interest_urls:
            query |= Q(**{
                'json__om:featureOfInterest__FeatureOfInterest__namedRegion__contains': [
                    {'@xlink:href': url}
                ]
            })
        return self.filter(query)

    def referencing_computation_type_urls(self, computation_type_urls: list):
        """Data Collections referencing at least one URL
        from a list of Computation Type URLs.
        """
        if not computation_type_urls:
            return self.none()
        query = Q()
        for url in computation_type_urls:
            query |= Q(**{'json__type__contains': [{'@xlink:href': url}]})
        return self.filter(query)
    
    def referencing_instrument_type_urls(self, instrument_type_urls: list):
        """Data Collections referencing at least one URL
        from a list of Instrument Type URLs.
        """
        if not instrument_type_urls:
            return self.none()
        query = Q()
        for url in instrument_type_urls:
            query |= Q(**{'json__type__contains': [{'@xlink:href': url}]})
        return self.filter(query)

    def referencing_annotation_type_urls(self, annotation_type_urls: list):
        if not annotation_type_urls:
            return self.none()
        query = Q()
        for url in annotation_type_urls:
            query |= Q(**{'json__type__contains': [{'@xlink:href': url}]})
        return self.filter(query)
    
    def referencing_party_url(self, party_url: str):
        """Data Collections referencing a given Organisation
        or Individual URL.
        """
        return self.filter(**{
            'json__relatedParty__contains': [
                {
                    'ResponsiblePartyInfo': {
                        'party': {'@xlink:href': party_url}
                    }
                }
            ]
        })
    
    def referencing_process_url(self, process_url: str):
        """Data Collections referencing a given Process URL.
        """
        return self.filter(**{'json__om:procedure__@xlink:href': process_url})

    def referencing_process_urls(self, process_urls: list):
        """Data Collections referencing at least one URL
        from a list of Process URLs.
        """
        if not process_urls:
            return self.none()
        query = Q()
        for url in process_urls:
            query |= Q(**{'json__om:procedure__@xlink:href': url})
        return self.filter(query)
    
    def referencing_project_url(self, project_url: list):
        """Data Collections referencing a given Project URL.
        """
        return self.filter(**{
            'json__project__contains': [
                {'@xlink:href': project_url}
            ]
        })

    def for_search_by_feature_of_interest_urls(self, feature_of_interest_urls: list):
        return self.referencing_feature_of_interest_urls(feature_of_interest_urls)

    def for_search_by_instrument_type_urls(self, instrument_type_urls: list, process_urls: list):
        return self.referencing_instrument_type_urls(instrument_type_urls) \
            | self.referencing_process_urls(process_urls)

    def for_search_by_computation_type_urls(self, computation_type_urls: list, process_urls: list):
        return self.referencing_computation_type_urls(computation_type_urls) \
            | self.referencing_process_urls(process_urls)

    def for_search_by_annotation_type_urls(self, annotation_type_urls: list):
        return self.referencing_annotation_type_urls(annotation_type_urls)

    def for_search_by_observed_property_urls(self, process_urls: list):
        return self.referencing_process_urls(process_urls)

    def for_final_search_step(
            self,
            data_collections_found_by_feature_of_interest,
            data_collections_found_by_instrument_type,
            data_collections_found_by_computation_type,
            data_collections_found_by_annotation_type,
            data_collections_found_by_observed_property,
            feature_of_interest_urls: list = [],
            instrument_type_urls: list = [],
            computation_type_urls: list = [],
            annotation_type_urls: list = [],
            observed_property_urls: list = []):
        if (not data_collections_found_by_feature_of_interest
            and not data_collections_found_by_instrument_type
            and not data_collections_found_by_computation_type
            and not data_collections_found_by_annotation_type
            and not data_collections_found_by_observed_property):
            return self.none()
        search_results = self.all()
        if feature_of_interest_urls:
            search_results &= data_collections_found_by_feature_of_interest
        if instrument_type_urls:
            search_results &= data_collections_found_by_instrument_type
        if computation_type_urls:
            search_results &= data_collections_found_by_computation_type
        if annotation_type_urls:
            search_results &= data_collections_found_by_annotation_type
        if observed_property_urls:
            search_results &= data_collections_found_by_observed_property
        return search_results

    def for_search(
            self,
            process_urls: list,
            feature_of_interest_urls: list,
            instrument_type_urls: list,
            computation_type_urls: list):
        """Data Collections meeting at least one of the following
        criteria:
        * Referencing at least one URL from a
          list of Process URLs
        * Referencing at least one URL from a
          list of Feature of Interest URLs
        * Referencing at least one URL from
          a list of Instrument Type URLs
        * Referencing at least one URL from a
          list of Computation Type URLs
        """
        search_results = self.all()
        results_referencing_process_urls = self.referencing_process_urls(process_urls)
        results_referencing_instrument_type_urls = self.referencing_instrument_type_urls(
            instrument_type_urls
        )
        results_referencing_computation_type_urls = self.referencing_computation_type_urls(
            computation_type_urls
        )
        results_referencing_feature_of_interest_urls = self.referencing_feature_of_interest_urls(
            feature_of_interest_urls
        )

        if process_urls:
            search_results &= results_referencing_process_urls
        if instrument_type_urls:
            search_results &= results_referencing_instrument_type_urls
        if computation_type_urls:
            search_results &= results_referencing_computation_type_urls
        if feature_of_interest_urls:
            search_results &= results_referencing_feature_of_interest_urls

        return search_results

    def for_delete_chain(self, metadata_server_url: str):
        """Data Collections referencing a URL corresponding
        to a metadata registration that is planned for deletion.
        """
        referencing_party_url = self.referencing_party_url(metadata_server_url)
        referencing_project_url = self.referencing_project_url(metadata_server_url)
        referencing_process_url = self.referencing_process_url(metadata_server_url)
        return referencing_party_url | referencing_project_url | referencing_process_url


class StaticDatasetEntryQuerySet(ScientificMetadataQuerySet):
    def referencing_feature_of_interest_urls(self, feature_of_interest_urls: list):
        """Static Dataset Entries referencing at least one URL
        from a list of Feature of Interest URLs.
        """
        if not feature_of_interest_urls:
            return self.none()
        query = Q()
        for url in feature_of_interest_urls:
            query |= Q(**{
                'json__featureOfInterest__namedRegion__contains': [
                    {'@xlink:href': url}
                ]
            })
        return self.filter(query)

    def for_search(self, feature_of_interest_urls: list):
        """Static Dataset Entries referencing at least one URL
        from a list of Feature of Interest URLs."""
        return self.referencing_feature_of_interest_urls(feature_of_interest_urls)

    def for_delete_chain(self, metadata_server_url: str):
        """Static Dataset Entries referencing a URL corresponding
        to a metadata registration that is planned for
        deletion.
        """
        return []


class DataSubsetQuerySet(ScientificMetadataQuerySet):
    def referencing_static_dataset_entry_url(self, static_dataset_entry_url: str):
        """Data Subsets referencing a given Static Dataset
        Entry URL.
        """
        query = Q()
        query |= Q(**{
            'json__entryIdentifier__@xlink:href': static_dataset_entry_url
        })
        query |= Q(**{
            'json__entryIdentifier__contains': [
                {'@xlink:href': static_dataset_entry_url}
            ]
        })
        return self.filter(query)

    def referencing_data_collection_url(self, data_collection_url: str):
        """Data Subsets referencing a given Data Collection URL.
        """
        return self.filter(**{
            'json__dataCollection__@xlink:href': data_collection_url
        })

    def for_delete_chain(self, metadata_server_url: str):
        """Data Subsets referencing a URL
        corresponding to a metadata registration that
        is planned for deletion.
        """
        referencing_data_collection_url = self.referencing_data_collection_url(
            metadata_server_url
        )
        referencing_static_dataset_entry_url = self.referencing_static_dataset_entry_url(
            metadata_server_url
        )
        return referencing_data_collection_url | referencing_static_dataset_entry_url


class WorkflowQuerySet(ScientificMetadataQuerySet):
    def referencing_data_collection_urls(self, data_collection_urls: list[str]):
        """Workflows referencing at least one URL
        from a list of Data Collection URLs."""
        if not data_collection_urls:
            return self.none()
        query = Q()
        for url in data_collection_urls:
            query |= Q(**{
                'json__dataCollection__contains': [
                    {'@xlink:href': url}
                ]
            })
        return self.filter(query)


class HandleURLMappingQuerySet(models.QuerySet):
    def for_url(self, url):
        """Handle to URL mappings for a given URL. One
        URL may be registered with many handles.
        """
        return self.filter(url=url)
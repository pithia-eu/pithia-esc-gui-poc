from abc import ABC, abstractmethod
from django.urls import reverse_lazy


class classproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class AbstractHelpArticleContent(ABC):
    @classproperty
    @abstractmethod
    def title(self):
        pass

    @classproperty
    @abstractmethod
    def functionality(self):
        return None

    @classproperty
    @abstractmethod
    def hover_text(self):
        pass

    @classproperty
    @abstractmethod
    def links(self):
        return []

    @classproperty
    @abstractmethod
    def closely_related_links(self):
        return []

    @classproperty
    @abstractmethod
    def broadly_related_links(self):
        return []

    @classproperty
    @abstractmethod
    def related_guides(self):
        return []

    @classproperty
    @abstractmethod
    def related_functionalities(self):
        return []

    @classproperty
    @abstractmethod
    def article_url(self):
        pass

    @classproperty
    @abstractmethod
    def dialog_id(self):
        pass
    
    @classmethod
    def as_dict(cls):
        return {
            'title': cls.title,
            'functionality': cls.functionality,
            'hover_text': cls.hover_text,
            'links': cls.links,
            'closely_related_links': cls.closely_related_links,
            'broadly_related_links': cls.broadly_related_links,
            'related_guides': cls.related_guides,
            'related_functionalities': cls.related_functionalities,
            'article_url': cls.article_url,
            'dialog_id': cls.dialog_id,
        }


class DataCollectionsHelpArticleContent(AbstractHelpArticleContent):
    title = 'Data Collections'
    functionality = ('Data Collections', reverse_lazy('browse:list_data_collections'))
    hover_text = 'List of all Data Collections in e-Science Centre.'
    closely_related_links = [
        ('Search by Content', reverse_lazy('help:search_data_collections_by_content')),
        ('Simple Search', reverse_lazy('help:data_collection_simple_search')),
    ]
    related_guides = [
        ('Data Registration Guide', reverse_lazy('resource_registration_user_guide')),
    ]
    article_url = reverse_lazy('help:data_collections')
    dialog_id = 'dialog-data-collections-help'


class DataCollectionsSimpleSearchHelpArticleContent(AbstractHelpArticleContent):
    title = 'Data Collection Simple Search'
    functionality = ('Data Collection Simple Search', reverse_lazy('simple_search:index'))
    hover_text = 'Search relevant Data Collections by looking for matching words in various free-text metadata descriptions.'
    closely_related_links = [
        ('Search Data Collections by Content', reverse_lazy('help:search_data_collections_by_content')),
    ]
    related_functionalities = [
        ('Data Collection-related Metadata', reverse_lazy('browse:data_collection_related_resource_types')),
    ]
    article_url = reverse_lazy('help:data_collection_simple_search')
    dialog_id = 'dialog-simple-search-help'


class GgusRaiseATicketHelpArticleContent(AbstractHelpArticleContent):
    title = 'Raising a Ticket'
    hover_text = None
    related_functionalities = [
        ('Help & Support', reverse_lazy('support')),
    ]
    article_url = reverse_lazy('help:ggus_raise_a_ticket')
    dialog_id = None


class SearchDataCollectionsByContentHelpArticleContent(AbstractHelpArticleContent):
    title = 'Search Data Collections by Content'
    functionality = ('Search Data Collections by Content', reverse_lazy('data_collection_search:index'))
    hover_text = 'Search relevant Data Collections by selecting desired data content (feature of interest, instrument, model or annotation type, observed property).'
    closely_related_links = [
        ('Simple Search', reverse_lazy('help:data_collection_simple_search')),
    ]
    related_functionalities = [
        ('Data Collection-related Metadata', reverse_lazy('browse:data_collection_related_resource_types')),
        ('Space Physics Ontology', reverse_lazy('ontology:index')),
    ]
    article_url = reverse_lazy('help:search_data_collections_by_content')
    dialog_id = 'dialog-search-by-content-help'
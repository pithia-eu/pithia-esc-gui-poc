from abc import ABC, abstractmethod
from django.urls import reverse_lazy


class classproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class HelpArticleContent(ABC):
    @classproperty
    @abstractmethod
    def title(self):
        pass

    @classproperty
    @abstractmethod
    def hover_text(self):
        pass

    @classproperty
    @abstractmethod
    def main_text(self):
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
    def article_url(self):
        pass
    
    @classmethod
    def as_dict(cls):
        return {
            'title': cls.title,
            'hover_text': cls.hover_text,
            'main_text': cls.main_text,
            'links': cls.links,
            'closely_related_links': cls.closely_related_links,
            'broadly_related_links': cls.broadly_related_links,
            'article_url': cls.article_url,
        }

class DataCollectionsHelpArticleContent(HelpArticleContent):
    title = 'Data Collections'
    hover_text = 'List of all Data Collections in e-Science Centre.'
    main_text = '''
        <p>The e-Science Center holds <strong>metadata documents</strong> that describe a wide variety of <strong>Data Collections</strong> relevant to PITHIA-NRF.
        Data Collections can be sensor measurements, outputs of numerical models, computed indicators of helio- and geospace activity.
        They can be <strong>pre-computed</strong> (stored as permanent datasets) or <strong>run on-demand</strong> with custom parameters.
        The data access can be provided by the <strong>original data owners</strong> using their resources (web pages, standardized API calls) or by <strong>running installed models</strong> at eSC computer park.</p>
        <p><strong>The &quot;All Data Collections&quot; function lists all collections</strong>, sorted alphabetically by their name.</p>

    '''
    closely_related_links = [
        ('Search by Content', reverse_lazy('help:search_data_collections_by_content')),
        ('Simple Search', reverse_lazy('help:data_collection_simple_search')),
    ]
    broadly_related_links = [
        ('Data Registration Guide', reverse_lazy('resource_registration_user_guide')),
    ]
    article_url = reverse_lazy('help:data_collections')

class SearchDataCollectionsByContentHelpArticleContent(HelpArticleContent):
    title = 'Search Data Collections by Content'
    hover_text = 'Search relevant Data Collections by selecting desired data content (feature of interest, instrument or model type, observed property).'
    main_text = '''
        <p>The e-Science Centre holds <strong>metadata documents</strong> that describe a wide variety of <strong>Data Collections</strong> relevant to PITHIA-NRF.
        A subset of relevant Data Collection may be retrieved for inspection by specifying various search criteria.</p>
        <p><strong>The &quot;Search Data Collections by content&quot; uses standard dictionary terms</strong> to find data of relevant content.</p>
        <p>Each Data Collection is registered using standard terminology to describe it. The terminology includes (a) PITHIA schema based on the <em>science-neutral</em> ISO 19156:2023 standard for Observations and Measurements and (b) <em>Space Physics specific</em> dictionaries of the standard terms (Ontology).</p>
        <p>Search Data Collections by content presents selectable items in the schema and ontology dictionaries to locate data collections of interest.
        The PITHIA schema items include: 1. Feature of Interest, 2. Computation and Instrument types, and 3. Observed Property.
        Ontology provides standard terms for the check-boxes under 1, 2, and 3.</p>


    '''
    closely_related_links = [
        ('Simple Search', reverse_lazy('help:data_collection_simple_search')),
    ]
    broadly_related_links = [
        ('Space Physics Ontology', reverse_lazy('resource_registration_user_guide')),
        ('All Scientific Metadata', reverse_lazy('resource_registration_user_guide')),
    ]
    article_url = reverse_lazy('help:data_collections')
from abc import ABC, abstractmethod
from django.urls import reverse_lazy


class HelpArticleContent(ABC):
    @property
    @abstractmethod
    def dialog_text(self):
        pass

    @property
    @abstractmethod
    def main_text(self):
        pass

    @property
    @abstractmethod
    def closely_related_links(self):
        pass

    @property
    @abstractmethod
    def broadly_related_links(self):
        pass

class DataCollectionsHelpArticleContent(HelpArticleContent):
    dialog_text = 'List of all Data Collections in e-Science Centre.'
    main_text = '''
        <p>
            The e-Science Centre holds <em>metadata documents</em> that describe a wide variety of <em>Data Collections</em> relevant to PITHIA-NRF.
            Data Collections can be sensor measurements, outputs of numerical models, computed indicators of helio- and geospace activity.
            They can be <em>pre-computed</em> (stored as permanent datasets) or <em>run on-demand</em> with custom parameters.
            The data access can be provided by the <em>original data owners</em> using their resources (web pages, standardized API calls) or by
            <em>running installed models</em> at eSC computer park.
        </p>
        <p>
            The <em>"All Data Collections" function lists all collections</em>, sorted alphabetically by their name.
        </p>
    '''
    closely_related_links = [
        ('Search by Content', reverse_lazy('help:search_data_collections_by_content')),
        ('Simple Search', reverse_lazy('help:data_collection_simple_search')),
    ]
    broadly_related_links = [
        ('Data Registration Guide', reverse_lazy('resource_registration_user_guide')),
    ]
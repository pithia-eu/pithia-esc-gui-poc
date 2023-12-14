from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

def index(request):
    return render(request, 'help/index.html', {
        'title': 'Help'
    })

class HelpArticleView(TemplateView):
    template_name = 'help/article.html'

    title = 'Add title here'
    hover_text = ''
    introduction = ''
    description = ''
    main_text = ''
    links = ''
    closely_related_links = []
    broadly_related_links = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['hover_text'] = self.hover_text
        context['description'] = self.description
        context['introduction'] = self.introduction
        context['main_text'] = self.main_text
        context['links'] = self.links
        context['closely_related_links'] = self.closely_related_links
        context['broadly_related_links'] = self.broadly_related_links
        return context

class SearchDataCollectionsByContentHelpArticleView(HelpArticleView):
    def get(self, request, *args, **kwargs):
        self.title = 'Search Data Collections by Content'
        self.hover_text = '''
        <p>
            Search for Data Collections with Features of Interest, Computation Types, Instruments Types or Observed Properties.
        </p>
        <p>
            These must all be from the <a href="/ontology/guide">Space Physics Ontology</a>.
        </p>
        '''
        return super().get(request, *args, **kwargs)

class DataCollectionSimpleSearchHelpArticleView(HelpArticleView):
    def get(self, request, *args, **kwargs):
        self.title = 'Data Collection Simple Search'
        self.hover_text = '''
        <p>
            Description coming soon.
        </p>
        '''
        return super().get(request, *args, **kwargs)

class DataCollectionsHelpArticleView(HelpArticleView):
    def get(self, request, *args, **kwargs):
        self.title = 'Data Collections'
        self.hover_text = '''
            <p>
                List of all Data Collections in e-Science Centre.
            </p>
        '''
        self.main_text = '''
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
        return super().get(request, *args, **kwargs)

class CataloguesHelpArticleView(HelpArticleView):
    def get(self, request, *args, **kwargs):
        self.title = 'Catalogues'
        self.hover_text = '''
        <p>
            Description coming soon.
        </p>
        '''
        return super().get(request, *args, **kwargs)

class AllScientificHelpArticleView(HelpArticleView):
    def get(self, request, *args, **kwargs):
        self.title = 'All Scientific Metadata'
        self.hover_text = '''
        <p>
            Description coming soon.
        </p>
        '''
        return super().get(request, *args, **kwargs)
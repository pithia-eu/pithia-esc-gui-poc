from django.shortcuts import render
from django.views.generic import TemplateView

from .services import (
    DataCollectionsHelpArticleContent,
    DataCollectionsSimpleSearchHelpArticleContent,
    GgusRaiseATicketHelpArticleContent,
    SearchDataCollectionsByContentHelpArticleContent,
)

# Create your views here.

def index(request):
    return render(request, 'help/index.html', {
        'title': 'Help'
    })


class HelpArticleView(TemplateView):
    template_name = 'help/articles/base.html'

    help_article_content = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.help_article_content.title} Help'
        context['help_topic'] = self.help_article_content.title
        context['hover_text'] = self.help_article_content.hover_text
        context['links'] = self.help_article_content.links
        context['closely_related_links'] = self.help_article_content.closely_related_links
        context['broadly_related_links'] = self.help_article_content.broadly_related_links
        context['related_guides'] = self.help_article_content.related_guides
        context['related_functionalities'] = self.help_article_content.related_functionalities
        return context


class DataCollectionsHelpArticleView(HelpArticleView):
    template_name = 'help/articles/data_collections.html'
    help_article_content = DataCollectionsHelpArticleContent


class DataCollectionSimpleSearchHelpArticleView(HelpArticleView):
    template_name = 'help/articles/data_collection_simple_search.html'
    help_article_content = DataCollectionsSimpleSearchHelpArticleContent


class GgusRaiseATicketHelpArticleView(HelpArticleView):
    template_name = 'help/articles/ggus_raise_a_ticket.html'
    help_article_content = GgusRaiseATicketHelpArticleContent


class SearchDataCollectionsByContentHelpArticleView(HelpArticleView):
    template_name = 'help/articles/search_data_collections_by_content.html'
    help_article_content = SearchDataCollectionsByContentHelpArticleContent
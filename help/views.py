from django.shortcuts import render
from django.views.generic import TemplateView

from .services import (
    DataCollectionsHelpArticleContent,
    DataCollectionsSimpleSearchHelpArticleContent,
    SearchDataCollectionsByContentHelpArticleContent,
)

# Create your views here.

def index(request):
    return render(request, 'help/index.html', {
        'title': 'Help'
    })

class HelpArticleView(TemplateView):
    template_name = 'help/article.html'

    help_article_content = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.help_article_content.title
        context['hover_text'] = self.help_article_content.hover_text
        context['main_text'] = self.help_article_content.main_text
        context['links'] = self.help_article_content.links
        context['closely_related_links'] = self.help_article_content.closely_related_links
        context['broadly_related_links'] = self.help_article_content.broadly_related_links
        return context

class SearchDataCollectionsByContentHelpArticleView(HelpArticleView):
    help_article_content = SearchDataCollectionsByContentHelpArticleContent

class DataCollectionSimpleSearchHelpArticleView(HelpArticleView):
    help_article_content = DataCollectionsSimpleSearchHelpArticleContent

class DataCollectionsHelpArticleView(HelpArticleView):
    help_article_content = DataCollectionsHelpArticleContent
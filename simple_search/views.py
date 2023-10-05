from django.shortcuts import render

from .forms import SimpleSearchForm
from .services import find_data_collections_for_simple_search

_INDEX_PAGE_TITLE = 'Data Collection Simple Search'


# Create your views here.
def index(request):
    form = SimpleSearchForm()

    return render(request, 'simple_search/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'form': form,
    })

def results(request):
    query = request.POST.get('query')

    form = SimpleSearchForm(initial={'query': query})
    results = find_data_collections_for_simple_search(query)

    return render(request, 'simple_search/results.html', {
        'title': 'Results',
        'results': results,
        'form': form,
        'query': query,
        'simple_search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })
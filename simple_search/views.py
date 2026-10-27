from django.contrib import messages
from django.shortcuts import (
    redirect,
    render,
)

from .forms import SimpleSearchForm
from .services import find_data_collections_for_simple_search

_INDEX_PAGE_TITLE = 'Data Collection Simple Search'


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SimpleSearchForm(request.POST)
        
        if not form.is_valid():
            messages.error('The search query submitted was not valid.')
            return redirect('simple_search:index')

        request.session.update({
            'simple_search': {
                'query': form.cleaned_data.get('query'),
                'is_exact': form.cleaned_data.get('exact'),
            }
        })
        return redirect('simple_search:results')
        
    form = SimpleSearchForm()

    return render(request, 'simple_search/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'form': form,
    })

def results(request):
    search_parameters = request.session.get('simple_search')
    query = search_parameters.get('query')
    is_exact = search_parameters.get('is_exact')

    results = []
    form = SimpleSearchForm()
    if query:
        form = SimpleSearchForm(initial={'query': query, 'exact': is_exact})
        results = find_data_collections_for_simple_search(query, exact=is_exact)

    return render(request, 'simple_search/results.html', {
        'title': 'Data Collection Simple Search Results',
        'results': results,
        'form': form,
        'query': query,
        'exact': is_exact,
        'simple_search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })
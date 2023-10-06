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
        
        request.session['query'] = form.cleaned_data.get('query')
        return redirect('simple_search:results')
        
    form = SimpleSearchForm()

    return render(request, 'simple_search/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'form': form,
    })

def results(request):
    query = request.session.get('query')

    results = []
    form = SimpleSearchForm()
    if query:
        form = SimpleSearchForm(initial={'query': query})
        results = find_data_collections_for_simple_search(query)

    return render(request, 'simple_search/results.html', {
        'title': 'Results',
        'results': results,
        'form': form,
        'query': query,
        'simple_search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })
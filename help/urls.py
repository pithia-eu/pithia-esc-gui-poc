from django.urls import path

from . import views

app_name = 'help'
urlpatterns = [
    path('', views.index, name='index'),
    path('search-data-collections-by-content/', views.SearchDataCollectionsByContentHelpArticleView.as_view(), name='search_data_collections_by_content'),
    path('data-collection-simple-search/', views.DataCollectionSimpleSearchHelpArticleView.as_view(), name='data_collection_simple_search'),
    path('data-collections/', views.DataCollectionsHelpArticleView.as_view(), name='data_collections'),
    path('catalogues/', views.CataloguesHelpArticleView.as_view(), name='catalogues'),
    path('all-scientific-metadata/', views.AllScientificHelpArticleView.as_view(), name='all_scientific_metadata'),
]

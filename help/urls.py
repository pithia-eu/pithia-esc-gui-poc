from django.urls import path

from . import views

app_name = 'help'
urlpatterns = [
    path('', views.index, name='index'),
    path('search-data-collections-by-content/', views.SearchDataCollectionsByContentHelpArticleView.as_view(), name='search_data_collections_by_content'),
    path('data-collection-simple-search/', views.DataCollectionSimpleSearchHelpArticleView.as_view(), name='data_collection_simple_search'),
    path('data-collections/', views.DataCollectionsHelpArticleView.as_view(), name='data_collections'),
    path('raise-a-ticket/', views.GgusRaiseATicketHelpArticleView.as_view(), name='ggus_raise_a_ticket'),
]

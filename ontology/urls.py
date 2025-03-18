from django.urls import path

from . import views

app_name = 'ontology'
urlpatterns = [
    path('', views.ontology, name='index'),
    path('guide/', views.ontology_guide, name='guide'),
    path('categories/<category>/', views.ontology_category_terms_list, name='ontology_category_terms_list'),
    path('categories/<category>/terms/', views.ontology_category_terms_list_only, name='ontology_category_terms_list_only'),
    path('categories/observedProperty/terms/<term_id>/', views.ObservedPropertyTermDetailView.as_view(), name='observed_property_term_detail'),
    path('categories/licence/terms/<term_id>/', views.LicenceTermDetailView.as_view(), name='licence_term_detail'),
    path('categories/<category>/terms/<term_id>/', views.OntologyTermDetailView.as_view(), name='ontology_term_detail'),
]

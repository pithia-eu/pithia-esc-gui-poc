from django.urls import path

from . import views

app_name = 'ontology'
urlpatterns = [
    path('', views.ontology, name='index'),
    path('categories/<category>/', views.ontology_category_terms_list, name='ontology_category_terms_list'),
    path('categories/<category>/terms/', views.ontology_category_terms_list_only, name='ontology_category_terms_list_only'),
    path('categories/<category>/terms/<term_id>/', views.ontology_term_detail, name='ontology_term_detail'),
]

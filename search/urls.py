from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('by-feature-of-interest/', views.results_from_foi, name='results_from_foi'),
    path('results/', views.results, name='results'),
    path('templates/form/component/<ontology_component>/', views.get_tree_form_for_ontology_component)
]

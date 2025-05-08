from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('templates/form/component/<ontology_component>/', views.get_tree_form_for_ontology_component)
]

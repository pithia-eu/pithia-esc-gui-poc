from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('foi-selection/', views.foi_selection, name='foi_selection'),
    path('comp-and-instr-type-selection/', views.comp_and_instr_type_selection, name='comp_and_instr_type_selection'),
    path('op-selection/', views.op_selection, name='op_selection'),
    path('results/', views.results, name='results'),
    path('templates/form/component/<ontology_component>/', views.get_tree_form_for_ontology_component)
]

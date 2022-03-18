from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('<ontology_component>/', views.get_checkbox_tree_for_ontology_component)
]

from django.urls import path

from . import views

app_name = 'workflow_search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('templates/<ontology_branch_name>/', views.search_form_template, name='search_form_template'),
]

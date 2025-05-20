from django.urls import path

from . import views

app_name = 'static_dataset_search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('form-templates/features-of-interest/', views.foi_form_template, name='foi_form_template'),
]

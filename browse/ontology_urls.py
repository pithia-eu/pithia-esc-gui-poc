from django.urls import path

from . import views

app_name = ''
urlpatterns = [
    path('', views.ontology, name='ontology'),
    path('<category>/', views.ontology_category_terms_list, name='ontology_category_terms_list'),
    path('<category>/<term_id>/', views.ontology_term_detail, name='ontology_term_detail'),
]

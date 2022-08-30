from django.urls import path

from . import views

app_name = ''
urlpatterns = [
    path('', views.ontology, name='ontology'),
    path('<category>/<term_id>', views.ontology, name='ontology_detail'),
]

from django.urls import include, path

from . import views

app_name = 'workflow_search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('form-templates/', include('workflow_search.form_urls'))
]

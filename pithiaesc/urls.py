from django.contrib import admin
from django.urls import include, path
from . import views

from browse.views import schemas

urlpatterns = [
    path('', views.index, name='home'),
    path('logout/', views.logout, name='logout'),
    # Include URLs
    path('', include('browse.urls')),
    path('', include('present.urls')),
    path('', include('user_management.urls')),
    path('', include('utils.urls')),
    path('ontology/', include('ontology.urls')),
    path('search/', include('data_collection_search.urls')),
    path('simple-search/', include('simple_search.urls')),
    path('static-dataset-search/', include('static_dataset_search.urls')),
    path('workflow-search/', include('workflow_search.urls')),
    path('help/', include('help.urls')),
    path('admin/', admin.site.urls),
    path('schemas/', schemas, name='schemas'),
    path('data-collection-registration-guide', views.data_collection_registration_guide, name='data_collection_registration_guide'),
    path('static-dataset-registration-guide', views.static_dataset_registration_guide, name='static_dataset_registration_guide'),
    path('workflow-registration-guide', views.workflow_registration_guide, name='workflow_registration_guide'),
    path('user-registration-guide', views.user_registration_guide, name='user_registration_guide'),
    path('terms-of-use', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('support', views.support, name='support'),
    path('authorised/', include('pithiaesc.secure_urls')),
]

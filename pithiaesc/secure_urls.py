from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index_admin, name='data_provider_home'),
    path('', include('update.urls')),
    path('', include('delete.urls')),
    path('', include('utils.urls')),
    path('manage/', include('resource_management.urls')),
    path('register/', include('register.urls')),
]

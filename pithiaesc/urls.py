from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin-home/', views.index_admin, name='home_admin'),
    path('', include('browse.urls')),
    path('', include('update.urls')),
    path('', include('delete.urls')),
    path('manage/', include('resource_management.urls')),
    path('search/', include('search.urls')),
    path('register/', include('register.urls')),
    path('validate/', include('validation.urls')),
    path('present/', include('present.urls')),
    path('admin/', admin.site.urls),
]

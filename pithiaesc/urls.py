from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('', include('browse.urls')),
    path('search/', include('search.urls')),
    path('present/', include('present.urls')),
    path('admin/', admin.site.urls),
    path('data-provider/', include('pithiaesc.secure_urls')),
]

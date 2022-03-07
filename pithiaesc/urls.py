from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('search/', include('search.urls')),
    path('admin/', admin.site.urls),
]

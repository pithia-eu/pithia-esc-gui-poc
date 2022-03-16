from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', include('search.urls')),
    path('register/', include('register.urls')),
    path('admin/', admin.site.urls),
]

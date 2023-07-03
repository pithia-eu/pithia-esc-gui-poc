from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', include('browse.urls')),
    path('ontology/', include('ontology.urls')),
    path('present/', include('present.urls')),
    path('search/', include('search.urls')),
    path('admin/', admin.site.urls),
    path('authorised/', include('pithiaesc.secure_urls')),
    path('', include('user_management.urls')),
]

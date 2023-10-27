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
    path('simple-search/', include('simple_search.urls')),
    path('admin/', admin.site.urls),
    path('data-resource-registration-guide', views.resource_registration_user_guide, name='resource_registration_user_guide'),
    path('terms-of-use', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('authorised/', include('pithiaesc.secure_urls')),
]

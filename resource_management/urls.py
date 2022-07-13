from django.urls import path

from . import views

app_name = 'resource_management'
urlpatterns = [
    path('', views.index, name='index'),
]

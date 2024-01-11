from django.urls import path

from . import views

app_name = 'workflows'
urlpatterns = [
    path('', views.index, name='index'),
]
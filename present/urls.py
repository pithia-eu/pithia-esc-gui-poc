from django.urls import path

from . import views

app_name = 'present'
urlpatterns = [
    path('', views.index, name='index')
]
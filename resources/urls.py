from django.urls import path

from . import views

app_name = 'resources'
urlpatterns = [
    path('', views.index, name='index'),
    path('<namespace>/<localID>/', views.detail, name='detail'),
]

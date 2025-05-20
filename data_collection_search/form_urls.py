from django.urls import path

from . import views

app_name = 'forms'
urlpatterns = [
    path('annotation-types/', views.AnnotationTypeSearchByContentTemplateView.as_view(), name='annotation_types'),
    path('computation-types/', views.ComputationTypeSearchByContentTemplateView.as_view(), name='computation_types'),
    path('features-of-interest/', views.FeatureOfInterestSearchByContentTemplateView.as_view(), name='features_of_interest'),
    path('instrument-types/', views.InstrumentTypeSearchByContentTemplateView.as_view(), name='instrument_types'),
    path('measurands/', views.MeasurandSearchByContentTemplateView.as_view(), name='measurands'),
    path('observed-properties/', views.ObservedPropertySearchByContentTemplateView.as_view(), name='observed_properties'),
    path('phenomenons/', views.PhenomenonSearchByContentTemplateView.as_view(), name='phenomenons'),
]

from django.urls import path

from . import views

app_name = 'validation'
urlpatterns = [
    path('api-specification-url/', views.api_specification_url, name='api_specification_url'),
    # Inline validation URLs
    path('new-registration/', views.QuickInlineRegistrationValidationFormView.as_view(), name='new_registration'),
    path('update/', views.QuickInlineUpdateValidationFormView.as_view(), name='update'),
    path('instrument-update/', views.QuickInlineInstrumentUpdateValidationFormView.as_view(), name='instrument_update'),
    path('xsd/', views.InlineXSDValidationFormView.as_view(), name='xsd'),
    path('new-localid/', views.localid, name='new_localid'),
]
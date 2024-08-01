import logging
from django.http import HttpResponse, HttpResponsePermanentRedirect


logger = logging.getLogger(__name__)


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Intended to work like Django's CommonMiddleware when the APPEND_SLASH
        # setting is set to True.
        # https://docs.djangoproject.com/en/5.0/ref/middleware/#django.middleware.common.CommonMiddleware
        # https://docs.djangoproject.com/en/5.0/ref/settings/#append-slash
        if request.path == '/health':
            return HttpResponsePermanentRedirect('/health/')

        if request.path == '/health/':
            return HttpResponse('OK')

        return self.get_response(request)


class ExceptionLoggingMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        logger.exception(exception)
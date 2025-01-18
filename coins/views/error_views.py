from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseNotFound, HttpResponseServerError
import logging

logger = logging.getLogger('django')

@requires_csrf_token
def handler404(request, exception=None):
    """
    Custom 404 error handler that provides more context to the error page.
    """
    context = {
        'request_path': request.path,
        'referer': request.META.get('HTTP_REFERER', None),
    }
    return HttpResponseNotFound(
        render(request, 'coins/404.html', context)
    )

@requires_csrf_token
def handler500(request, exception=None):
    """
    Custom 500 error handler that logs the error and provides a user-friendly error page.
    """
    if exception:
        logger.error(
            f"500 error at {request.path}",
            exc_info=exception,
            extra={
                'status_code': 500,
                'request': request,
            }
        )

    context = {
        'request_path': request.path,
    }
    return HttpResponseServerError(
        render(request, 'coins/500.html', context)
    )

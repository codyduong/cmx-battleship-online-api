import logging
from functools import wraps

from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated

from app.authentication import PlayerAuthentication
from app.exceptions import APIException


def app_exception_handler(f):
    """ decorator to catch and handle all exceptions """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIException as e:
            return e.response()
        except Exception as e:
            logging.error(f"encountered unexpected exception {e.__class__.__name__}: {str(e)}")
            return Response({"error": "Unexpected server error, please contact your system administrator."}, status=500)

    return decorated

def error_handling_view(methods):
    """ decorator to enable use with Django Views
    and handle exceptions provided by this package """
    def wrapper(func):
        return api_view(methods)(
            app_exception_handler(
                func
            )
        )
    return wrapper


def any_view(methods):
    """ view for unsecured requests
     includes error handling from morriswa package"""
    def wrapper(func):
        return error_handling_view(methods)(
            # override w_view to use no permission or authentication guards
            permission_classes([])(
                authentication_classes([])(
                    func
                )
            )
        )
    return wrapper


def session_view(methods):
    """ view for session requests
     includes error handling from morriswa package"""
    def wrapper(func):
        return error_handling_view(methods)(
            # override w_view to use session permission and authentication guards
            permission_classes([IsAuthenticated])(
                authentication_classes([PlayerAuthentication])(
                    func
                )
            )
        )
    return wrapper

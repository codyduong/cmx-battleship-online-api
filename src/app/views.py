from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes

from django_utils_morriswa.view_utils import w_view, WView

from app.authentication import PlayerAuthentication


class AnyView(WView):
    """ inherit this class to create a view for unsecured requests
     includes error handling from morriswa package"""
    authentication_classes = []
    permission_classes = []


def any_view(methods):
    """ view for unsecured requests
     includes error handling from morriswa package"""
    def wrapper(func):
        return w_view(methods)(
            # override w_view to use no permission or authentication guards
            permission_classes([])(
                authentication_classes([])(
                    func
                )
            )
        )
    return wrapper


class SessionView(WView):
    """ inherit this class to create a view for session requests
         includes error handling from morriswa package"""
    authentication_classes = [PlayerAuthentication]
    permission_classes = [IsAuthenticated]


def session_view(methods):
    """ view for session requests
     includes error handling from morriswa package"""
    def wrapper(func):
        return w_view(methods)(
            # override w_view to use session permission and authentication guards
            permission_classes([IsAuthenticated])(
                authentication_classes([PlayerAuthentication])(
                    func
                )
            )
        )
    return wrapper

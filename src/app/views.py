import app.authentication
import rest_framework.permissions

from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from django_utils_morriswa.view_utils import unsecured, w_view, WView


class AnyView(WView):
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
    authentication_classes = [app.authentication.PlayerAuthentication]
    permission_classes = [rest_framework.permissions.IsAuthenticated]


def session_view(methods):
    """ view for session requests
     includes error handling from morriswa package"""
    def wrapper(func):
        return w_view(methods)(
            # override w_view to use session permission and authentication guards
            permission_classes([rest_framework.permissions.IsAuthenticated])(
                authentication_classes([app.authentication.PlayerAuthentication])(
                    func
                )
            )
        )
    return wrapper


@any_view(['GET'])
def health(request):
    return Response({
        "msg": "hello world!"
    }, status=200)


@session_view(['GET'])
def shealth(request):
    return Response({
        "msg": f"hello {request.user.player_name}#{request.user.player_id}"
    }, status=200)

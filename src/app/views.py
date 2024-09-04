from typing import override

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app.authentication import PlayerAuthentication
from app.decorators import app_exception_handler, error_handling_view


class ErrorHandlingView(APIView):
    """ class to provide a Django View
    and handle exceptions provided by this package """
    @override
    @app_exception_handler
    def handle_exception(self, *args, **kwargs):
        return super(ErrorHandlingView, self).handle_exception(*args, **kwargs)


class AnyView(ErrorHandlingView):
    """ inherit this class to create a view for unsecured requests
     includes error handling from morriswa package"""
    authentication_classes = []
    permission_classes = []


class SessionView(ErrorHandlingView):
    """ inherit this class to create a view for session requests
         includes error handling from morriswa package"""
    authentication_classes = [PlayerAuthentication]
    permission_classes = [IsAuthenticated]

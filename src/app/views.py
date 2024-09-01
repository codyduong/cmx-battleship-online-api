from rest_framework.request import Request
from rest_framework.response import Response

from django_utils_morriswa.view_utils import unsecured, w_view

from app.permissions import is_admin


@w_view(['GET'])
@unsecured
def health(request):
    return Response({
        "msg": "hello world!"
    }, status=200)


@w_view(['GET'])
def shealth(request):
    return Response({
        "msg": "hello secure world!"
    }, status=200)

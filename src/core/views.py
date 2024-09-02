from rest_framework.request import Request
from rest_framework.response import Response

from app.views import any_view, session_view


@any_view(['GET'])
def health(request: Request) -> Response:
    """ health endpoint to test any_view """
    return Response({
        "msg": "hello world!"
    }, status=200)


@session_view(['GET'])
def shealth(request: Request) -> Response:
    """ health endpoint to test session_view """
    return Response({
        "msg": f"hello {request.user.player_name}#{request.user.player_id}"
    }, status=200)

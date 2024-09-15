from rest_framework.request import Request
from rest_framework.response import Response

from app.decorators import any_view, session_view

#Defines a health endpoint
@any_view(['GET'])
def health(request: Request) -> Response:
    """ health endpoint to test any_view """
    #returns a simple JSON response with message hello world 
    return Response({
        "msg": "hello world!"
    }, status=200)


@session_view(['GET'])
def shealth(request: Request) -> Response:
    """ health endpoint to test session_view """
    #Simple JSON response with message hello player_name and player_id
    return Response({
        "msg": f"hello {request.user.player_name}#{request.user.player_id}"
    }, status=200)

from rest_framework.request import Request
from rest_framework.response import Response
from user_session.models import LoginRequest
import user_session.daos as user_session_dao

from app.decorators import any_view, session_view

@any_view(['GET'])
def get_online_player_count(request: Request) -> Response:
    online_player_count = user_session_dao.get_online_player_count()
    return Response(status=200, data={
        'playerCount': online_player_count
    })

@any_view(['POST'])
def create_session_login(request: Request) -> Response:
    create_session_repr = LoginRequest(request.data)
    session_info = user_session_dao.start_session(create_session_repr)
    return Response(status=200, data=session_info)

@session_view(['DELETE'])
def destory_session_logout(request: Request) -> Response:
    session_id = request.user.session_id
    if session_id is not None:
        user_session_dao.end_session(session_id)
    return Response(status=204)

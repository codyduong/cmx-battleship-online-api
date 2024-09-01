from rest_framework.request import Request
from rest_framework.response import Response
from user_session.models import UserSession
from django_utils_morriswa.view_utils import w_view, unsecured
import user_session.daos as user_session_dao


@w_view(['POST'])
@unsecured
def create_session_login(request: Request) -> Response:
    create_session_repr = UserSession(request.data)
    session_info = user_session_dao.start_session(create_session_repr)
    return Response(status=200, data=session_info)

@w_view(['DELETE'])
def destory_session_logout(request: Request) -> Response:
    session_id = request.user.session_id
    if session_id is not None:
        user_session_dao.end_session(session_id)
    return Response(status=204)

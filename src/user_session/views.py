from rest_framework.request import Request
from rest_framework.response import Response
from user_session.models import UserSession

import user_session.daos as user_session_dao

from app.utils import AnyView


class UserSessionView(AnyView):

    @staticmethod
    def post(request: Request) -> Response:
        create_session_repr = UserSession(request.data)
        session_info = user_session_dao.start_session(create_session_repr)
        return Response(status=200, data=session_info)

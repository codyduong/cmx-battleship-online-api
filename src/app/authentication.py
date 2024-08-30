from rest_framework.authentication import BaseAuthentication


class SessionUser:
    def __init__(self, session_id, is_authenticated=False):
        self.session_id = session_id
        self.is_authenticated = is_authenticated


class SessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        session_id = request.headers.get('session-id')
        if not session_id:
            return None

        return SessionUser(session_id, True), session_id

from django.db import connections
from django.db.backends.postgresql.base import DatabaseWrapper
from psycopg2.extras import RealDictCursor


def cursor() -> RealDictCursor:
    conn: DatabaseWrapper = connections['default']
    conn.ensure_connection()
    return conn.connection.cursor(cursor_factory=RealDictCursor)

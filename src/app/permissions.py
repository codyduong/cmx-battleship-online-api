from django.contrib.auth.models import User

from app import connections


def is_admin(user: User) -> bool:
    result: any
    with connections.cursor() as db:
        db.execute("""
            select 1 
            from vet_admin admin
            left join user_profile profile
            on admin.profile_id = profile.profile_id
            where profile.auth_id = %s
        """, (user.username,))
        result = db.fetchone()

    return result is not None


def is_doctor(user: User) -> bool:
    result: any
    with connections.cursor() as db:
        db.execute("""
            select 1 
            from doctor
            left join user_profile profile
            on doctor.profile_id = profile.profile_id
            where profile.auth_id = %s
        """, (user.username,))
        result = db.fetchone()

    return result is not None

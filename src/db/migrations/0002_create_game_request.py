from django.db import migrations


class Migration(migrations.Migration):
    """
    creates the game request table 
    :author Timothy Holmes
    """
    dependencies = [(('db', '0001_create_user_session_table'))]
    operations = [
        migrations.RunSQL(
            sql="""create table game_request (
                game_request_id bigserial primary key, 
                player_invite_from char(4) not null, 
                player_invite_to char(4) not null,
                game_request_created timestamp not null,
                game_request_expiration timestamp not null
            );
            """,
            reverse_sql="""
                drop table game_request;
            """
        )
    ]

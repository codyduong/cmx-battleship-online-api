from django.db import migrations


class Migration(migrations.Migration):
    """
    creates the game request table 
    :author Timothy Holmes
    """
    dependencies = [(('user_session', '0001_create_user_session_table'))]
    operations = [
        migrations.RunSQL(
            sql="""create table game_request (
                game_request_id bigserial primary key, 
                player_invite_from char(4) not null unique, 
                player_invite_to varchar(32) not null,
                game_request_created timestamp not null default current_timestamp, 
                game_request_expiration timestamp not null default current_timestamp
            );
            """,
            reverse_sql="""
                drop table game_request;
            """
        )
    ]

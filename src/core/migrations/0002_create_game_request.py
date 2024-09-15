from django.db import migrations


class Migration(migrations.Migration):
    """
    creates the game request table 
    :author Timothy Holmes, William morris
    """
    #Finds the dependencies for 0002_create_game_request. 
    dependencies = [(('core', '0001_create_user_session_table'))]
    #Opertatios that need to be run during this migration
    operations = [
        migrations.RunSQL(
            #SQL command to create the game request table
            sql="""create table game_request (
                game_request_id bigserial primary key, 
                player_invite_from char(4) not null 
                    references user_session (player_id)
                    on delete cascade, 
                player_invite_to char(4) not null 
                    references user_session (player_id)
                    on delete cascade, 
                game_request_created timestamp not null default current_timestamp
            );
            """,
            #SQL statement to drop the table if the migration is reversed 
            reverse_sql="""
                drop table game_request;
            """
        )
    ]

from django.db import migrations


class Migration(migrations.Migration):
    """
    creates the game session
    :author Timothy Holmes
    """
    dependencies = [(('db', '0002_create_game_request'))]
    operations = [
        migrations.RunSQL(
            sql="""create table game_session (
                game_id uuid primary key, 
                player_one_id char(4) not null unique 
                    references user_session (player_id)
                    on delete cascade,
                player_two_id char(4) not null unique
                    references user_session (player_id)
                    on delete cascade, 
                active_turn char(2) not null check (active_turn in ('P1', 'P2')),
                num_ships char(1) not null check (num_ships in ('1', '2', '3', '4', '5')),
                game_started timestamp not null default current_timestamp,
                game_phase char(5) not null check (game_phase in ('SELCT','GOODG','P1WIN','P2WIN','NOWIN'))
            );
            """,
            reverse_sql="""
                drop table game_session;
            """
        )
    ]

from django.db import migrations


class Migration(migrations.Migration):
    """
    creates the game session
    :author Timothy Holmes
    """
    dependencies = [(('user_session', '0002_create_game_request'))]
    operations = [
        migrations.RunSQL(
            sql="""create table game_session (
                game_id uuid primary key, 
                player_one_id char(4) not null unique, 
                palyer_two_id char(4) not null unique,
                active_turn char(3) not null check (active_turn in ('one', 'two')),
                num_ships char(1) not null check(num_ships  between '1' and '5'),
                game_started timestamp not null default current_timestamp,
                game_ended timestamp not null, 
                game_phase char(4) not null check (game_phase in ('SELECT','P1WIN','P2WIN', 'NOWIN'))
            );
            """,
            reverse_sql="""
                drop table game_session;
            """
        )
    ]

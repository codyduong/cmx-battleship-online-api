from django.db import migrations


class Migration(migrations.Migration):
    """
    creates the user session table
    :author kevin rivers
    """
    dependencies = []
    operations = [
        migrations.RunSQL(
            sql="""
                create sequence player_id_seq
                INCREMENT 97
                MINVALUE 0
                MAXVALUE 9999
                START 0
                CYCLE;
                
                create table user_session (
                    session_id uuid primary key default gen_random_uuid(), 
                    player_id char(4) not null unique, 
                    player_name varchar(32) not null,
                    num_ships char(1) check (num_ships in ('1', '2', '3', '4' ,'5')),
                    session_started timestamp not null default current_timestamp, 
                    session_used timestamp
                );
            """,
            reverse_sql="""
                drop table user_session;
            """
        )
    ]

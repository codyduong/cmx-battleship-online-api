from django.db import migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunSQL(
            sql="""CREATE TABLE user_session (
                    session_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), 
                    player_id bigserial NOT NULL UNIQUE, 
                    player_name varchar(32) NOT NULL,
                    num_ships char(1) CHECK (num_ships IN ('1', '2', '3', '4' ,'5')),
                    session_started timestamp NOT NULL DEFAULT current_timestamp, 
                    session_used timestamp
                );
            """,
            reverse_sql="""
                DROP TABLE user_session;
            """
        )
    ]
from django.db import migrations


class Migration(migrations.Migration):
    """
    extends the game session table with state
    :author william morris
    """
    #Dependencies on other migrations
    dependencies = [(('core', '0003_create_game_session'))]
    #SQL command to add new column to game_session table
    operations = [
        migrations.RunSQL(
            #SQL command to add new column to game_session table
            sql="""
                alter table game_session
                add column game_state varchar(10000);
            """,
            #Reverse the migration for this column 
            reverse_sql="""
                alter table game_session
                drop column game_state;
            """
        )
    ]

from django.db import migrations


class Migration(migrations.Migration):
    """
    extends the game session table with state
    :author william morris
    """
    dependencies = [(('core', '0003_create_game_session'))]
    operations = [
        migrations.RunSQL(
            sql="""
                alter table game_session
                add column game_state varchar(10000);
            """,
            reverse_sql="""
                alter table game_session
                drop column game_state;
            """
        )
    ]

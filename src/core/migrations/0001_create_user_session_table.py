from django.db import migrations

#New migration class to create the user session table
#Inherits from djangos migrations class
class Migration(migrations.Migration):
    """
    Creates and fills Player Slot table
    Creates and applied trigger to manage player slots

    :authors kevin rivers, William Morris
    """
    #Finds any migrations that need to run first
    dependencies = []
    #operations that need to be run during this migration
    operations = [
        #Runs SQL commands as part of the migration
        migrations.RunSQL(
            sql="""
                -- William morris
                create table player_slot (
                    player_id char(4) not null unique,
                    in_use char(1) not null check (in_use in ('Y', 'N'))
                );
                
                -- Insert all possible player_id values from '0000' to '9999'
                -- William morris 
                -- Creates 10,000 player slots 
                DO $$
                DECLARE
                    i INTEGER;
                    player_id CHAR(4);
                BEGIN
                    -- Loops from 0 to 9999
                    FOR i IN 0..9999 LOOP
                        -- Convert i to a string and pad with zeros 
                        player_id := LPAD(i::TEXT, 4, '0');
                        -- Insert the player_id into the player_slot table with the generated player id
                        INSERT INTO player_slot (player_id, in_use) VALUES (player_id, 'N');
                    END LOOP;
                END $$;
                
                -- kevin rivers
                create table user_session (
                    session_id uuid primary key default gen_random_uuid(), 
                    player_id char(4) not null unique references player_slot (player_id),
                    player_name varchar(32) not null,
                    num_ships char(1) check (num_ships in ('1', '2', '3', '4' ,'5')),
                    session_started timestamp not null default current_timestamp, 
                    session_used timestamp not null default current_timestamp
                );
                
                -- William morris
                CREATE OR REPLACE FUNCTION update_player_slot_in_use()
                RETURNS TRIGGER AS $$
                BEGIN
                    -- Handle INSERT operation
                    IF (TG_OP = 'INSERT') THEN
                        UPDATE player_slot
                        SET in_use = 'Y'
                        WHERE player_id = NEW.player_id;
                
                    -- Handle DELETE operation
                    ELSIF (TG_OP = 'DELETE') THEN
                        UPDATE player_slot
                        SET in_use = 'N'
                        WHERE player_id = OLD.player_id;
                    END IF;
                    
                    RETURN null;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER user_session_ctrl_player_slot_trigger
                AFTER INSERT OR DELETE ON user_session
                FOR EACH ROW EXECUTE FUNCTION update_player_slot_in_use();
            """,
            reverse_sql="""
                drop trigger if exists user_session_ctrl_player_slot_trigger on user_session cascade;
                drop function if exists update_player_slot_in_use;
                drop table if exists user_session;
                drop table if exists player_slot;
            """
        )
    ]

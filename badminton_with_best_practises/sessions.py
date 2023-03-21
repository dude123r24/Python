# sessions.py
from datetime import datetime
from db import get_connection, get_cursor
from players import display_club_players, display_club_players_not_playing_today, display_club_players_playing_today
from psycopg2.errors import UniqueViolation
from utils import print_error, print_seperator_plus



# Select which players are playing in today's session
def sessions_players_select(club_id, session_id):
    players_playing = display_club_players_playing_today (club_id, session_id)

    players = display_club_players_not_playing_today (club_id, session_id)

    print("Select players playing today:")
    playing_today = []
    while True:
        player_id = input("Enter player ID (or '0' to finish): ")

        if player_id.lower() == '0':
            break

        try:
            player_id = int(player_id)
        except ValueError:
            print_error ("Invalid input. Please enter a valid player ID or '0' to finish.")
            continue

        player = next((player for player in players if player[0] == player_id), None)
        if player:
            if player_id not in playing_today:
                playing_today.append(player_id)
                print(f"Selected player: {player[1]}")
            else:
                print("Player already selected.")
        else:
            print_error ("Player not found. Please enter a valid player ID.")

    with get_connection() as conn:
        with get_cursor(conn) as cur:
            for player_id in playing_today:
                try:
                    cur.execute("""INSERT INTO sessions_players (session_id, player_id, active)
                                   VALUES (%s, %s, 'Y')""",
                                (session_id, player_id))
                except UniqueViolation as e:
                    print_error (f"Cannot add. Player {player_id} is already added to the session players.")
                    #print(f"Error: Cannot add. Player {player_id} is already added to the session players.")
                    conn.rollback()
                    continue
                except Exception as e:
                    print(f"Error: cannot add player {player_id} to session players: {e}")
                    conn.rollback()
                    continue
                else:
                    conn.commit()


    print("Players playing today:")
    for player_id in playing_today:
        player = next(player for player in players if player[0] == player_id)
        print(f"{player_id}. {player[1]}")


# Create a session
def create_session(club_id):
    now = datetime.now()

    with get_connection() as conn:
        with get_cursor(conn) as cur:
            # Get the latest season for the club
            cur.execute("""SELECT id FROM seasons WHERE club_id = %s
                           ORDER BY date_to DESC LIMIT 1""", (club_id,))
            season = cur.fetchone()

            # If there is no season for the club, you can either create one or return an error
            if not season:
                print("No season found for the club. Please create a season first.")
                return None

            season_id = season[0]

            # Check if a session already exists for today's date
            cur.execute("""SELECT id FROM sessions WHERE club_id = %s AND session_date = %s""",
                        (club_id, now.date()))
            existing_session = cur.fetchone()

            # If session already exists for today's date, return the existing session id
            if existing_session:
                return existing_session[0]

            # Get number of courts and players per court from club options
            cur.execute("""SELECT option_name, option_value FROM club_options
                           WHERE club_id = %s AND (option_name = 'num_courts' OR option_name = 'max_players_per_court')""",
                        (club_id,))
            options = dict(cur.fetchall())

            # Insert new session
            cur.execute("""INSERT INTO sessions (club_id, season_id, session_date, no_of_courts, no_of_players_per_court)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                           (club_id, season_id, now.date(), options['num_courts'], options['max_players_per_court']))
            session_id = cur.fetchone()[0]
            conn.commit()

    return session_id


def check_session_has_players(club_id, session_id):
    # Your implementation
    pass


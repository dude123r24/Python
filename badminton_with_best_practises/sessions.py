# sessions.py
from datetime import datetime
from db import get_connection, get_cursor

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
            
            cur.execute("""INSERT INTO sessions (club_id, season_id, session_date, no_of_courts, no_of_players_per_court)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                           (club_id, season_id, now.date(), 0, 0))  # Assuming no_of_courts and no_of_players_per_court as 0 initially
            session_id = cur.fetchone()[0]
            conn.commit()
            
    return session_id

def select_session_players(club_id, session_id):
    # Your implementation
    pass

def check_session_has_players(club_id, session_id):
    # Your implementation
    pass


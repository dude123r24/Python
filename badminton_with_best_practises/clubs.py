# clubs.py
from db import get_connection, get_cursor
from utils import print_seperator_tilda

def display_clubs():
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("SELECT id, name, city, country FROM clubs ORDER BY id")
            clubs = cur.fetchall()

            print(" ")
            print_seperator_tilda()
            print("Clubs:")
            for club in clubs:
                print(f"{club[0]}. {club[1]} ({club[2]}, {club[3]})")
            print("Press enter to exit")
            
def set_club(club_id):
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("SELECT name FROM clubs WHERE id = %s", (club_id,))
            club_name = cur.fetchone()

            if club_name:
                return club_name[0]
            else:
                print("Invalid club ID.")
                return None


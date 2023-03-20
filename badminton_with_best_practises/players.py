# players.py
from db import get_connection, get_cursor
from utils import print_seperator_tilda

def display_club_players(club_id):
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("""SELECT id, name
                           FROM players
                           WHERE id IN (SELECT player_id
                                        FROM players_clubs
                                        WHERE club_id = %s
                                          AND approved = true
                                          AND archived = false)
                           ORDER BY id""",
                        (club_id,))
            players = cur.fetchall()

            print_seperator_tilda()
            print("Club Players:")
            for player in players:
                print(f"{player[0]}. {player[1]}")

            return players

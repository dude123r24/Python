from tabulate import tabulate
from datetime import datetime, timedelta
from db import get_connection, get_cursor
from utils import print_seperator_tilda, print_seperator_star, print_error, print_info, print_table_header_seperator
from sessions import get_session_id, get_games_played_last_session_id

def report_session_no_of_games_per_player(club_id, season_id):
    session_id = input("Enter session ID (leave blank to get last session ID): ").strip()

    if not session_id:
        session_id = get_games_played_last_session_id(club_id)
    else:
        with get_connection() as conn:
            with get_cursor(conn) as cur:
                cur.execute("""
                    SELECT id FROM sessions
                    WHERE club_id = %s AND season_id = %s AND id = %s
                """, (club_id, season_id, session_id))
                if not cur.fetchone():
                    print_error(f"No games were played for this session ({session_id}) for this club.")
                    return

    with get_connection() as conn:
        with get_cursor(conn) as cur:
            # Get player session stats for the selected session_id
            cur.execute("""SELECT player_name, games_played, won, lost, win_percentage, minutes_since_last_game, session_rank
                        FROM player_stats_by_session
                        WHERE session_id = %s""",
                        (session_id,))
            player_stats = cur.fetchall()

            # Print results in tabular format
            print (" ")
            print_table_header_seperator(120)
            print("\033[1m{:<20} {:<15} {:<15} {:<15} {:<20} {:<20} {:<20}\033[0m".format(
                "Player", "Games Played", "Games Won", "Games Lost", "Win Percentage", "Mins, Last Game", "Rank"
            ))
            print_table_header_seperator(120)

            for stats in player_stats:
                # Replace None values with empty strings
                stats = tuple('' if value is None else value for value in stats)
                print("{:<20} {:<15} {:<15} {:<15} {:<20} {:<20} {:<20}".format(*stats))




def report_session_games_played(club_id, session_id):
    pass
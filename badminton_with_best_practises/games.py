# games.py

# Add other import statements here as needed

from db import get_connection, get_cursor
from utils import print_seperator_tilda, print_seperator_star

# Add other functions here as needed

def select_teams(club_id, session_id):
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            # Fetch the algorithm option from club_options table
            cur.execute("""SELECT option_value
                           FROM club_options
                           WHERE club_id = %s AND option_name = 'algorithm'""",
                        (club_id,))
            option_value = cur.fetchone()

            if option_value:
                algorithm = option_value[0]
            else:
                print("No algorithm found for this club.")
                return

            if algorithm == "random":
                select_teams_random(club_id, session_id)
            elif algorithm == "levels":
                select_teams_levels(club_id, session_id)
            else:
                print("Invalid algorithm option. Please set a valid algorithm for this club.")
                return

import random
from db import get_connection, get_cursor
from utils import print_seperator_tilda

def select_teams_random(club_id, session_id):
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("""SELECT players.id, players.name
                           FROM players
                           JOIN players_clubs ON players_clubs.player_id = players.id
                           WHERE players_clubs.club_id = %s
                             AND players.id NOT IN (
                               SELECT team1.player1_id FROM games
                               JOIN teams AS team1 ON games.team1_id = team1.team_id
                               WHERE games.session_id = %s AND games.game_end_time IS NULL
                               UNION ALL
                               SELECT team1.player2_id FROM games
                               JOIN teams AS team1 ON games.team1_id = team1.team_id
                               WHERE games.session_id = %s AND games.game_end_time IS NULL
                               UNION ALL
                               SELECT team2.player1_id FROM games
                               JOIN teams AS team2 ON games.team2_id = team2.team_id
                               WHERE games.session_id = %s AND games.game_end_time IS NULL
                               UNION ALL
                               SELECT team2.player2_id FROM games
                               JOIN teams AS team2 ON games.team2_id = team2.team_id
                               WHERE games.session_id = %s AND games.game_end_time IS NULL
                             )""",
                        (club_id, session_id, session_id, session_id, session_id))
            available_players = cur.fetchall()

    if len(available_players) < 2:
        print("Not enough players available to form the first team for a new game.")
        return

    # Select two random players and pair them
    player1, player2 = random.sample(available_players, 2)

    # Remove the players from TEAM1 selected above from available_players
    available_players = [player for player in available_players if player not in (player1, player2)]

    if len(available_players) < 2:
        print("Not enough players available to form a second team for a new game.")
        return

    # Select two random players and pair them
    player3, player4 = random.sample(available_players, 2)


    # Add the new teams to the teams table
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("""INSERT INTO teams (player1_id, player2_id)
                           VALUES (%s, %s) RETURNING team_id""",
                        (player1[0], player2[0]))
            team1_id = cur.fetchone()[0]

            cur.execute("""INSERT INTO teams (player1_id, player2_id)
                           VALUES (%s, %s) RETURNING team_id""",
                        (player3[0], player4[0]))
            team2_id = cur.fetchone()[0]
            conn.commit()
    
    print (" ")
    print_seperator_star()
    print(f"Session ID: {session_id}")
    print(f"Team 1: {player1[1]} and {player2[1]} (Team ID: {team1_id})")
    print("vs")
    print(f"Team 2: {player3[1]} and {player4[1]} (Team ID: {team2_id})")
    print_seperator_star()

    # Add a new game with the two teams in the games table
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("""INSERT INTO games (session_id, team1_id, team2_id, game_start_time, team1_score, team2_score)
                           VALUES (%s, %s, %s, NOW(), 0, 0) RETURNING id""",
                        (session_id, team1_id, team2_id))

            game_id = cur.fetchone()[0]
            conn.commit()

    print(f"New game started: Team 1 (ID: {team1_id}) vs Team 2 (ID: {team2_id}) (Game ID: {game_id})")



def select_teams_levels(club_id, session_id):
    # Add logic for team selection based on levels
    pass


def end_game():
    pass

def report_session_games_played(club_id, session_id):
    pass

def report_session_no_of_games_per_player(club_id, session_id):
    pass

def report_session_player_games_played(club_id, session_id):
    pass

def set_options(club_id, session_id):
    pass

def display_club_owner_details(club_id, session_id):
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("""SELECT p.id, p.name, p.email, p.phone
                           FROM players p
                           JOIN clubs c ON p.id = c.created_by
                           WHERE c.id = %s""", (club_id,))
            owner_details = cur.fetchone()

            if owner_details:
                print_seperator_tilda()
                print("Club Owner Details")
                print("ID:", owner_details[0])
                print("Name:", owner_details[1])
                print("Email:", owner_details[2])
                print("Phone:", owner_details[3])
            else:
                print("No owner details found for the club.")


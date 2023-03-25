# games.py

# Add other import statements here as needed

import random
from tabulate import tabulate
from datetime import datetime, timedelta
from db import get_connection, get_cursor
from utils import print_seperator_tilda, print_seperator_star, print_error, print_info
from players import get_player_name, display_player_stats, update_player_stats
from sessions import get_session_id, get_games_played_last_session_id


def select_teams(club_id, season_id, session_id):
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



def select_teams_levels(club_id, season_id, session_id):
    # Add logic for team selection based on levels
    pass


def end_game(club_id: int, season_id: int, session_id: int):
    session_id = get_session_id(club_id, season_id)
    print(f"Club ID: {club_id}, Season ID: {season_id}, Session_ID: {session_id}")

    games = get_ongoing_games(session_id)

    if not games:
        print("No games in progress.")
        return

    # print_info("Ongoing Games")
    # print("{:<10} {:<20} {:<20} {:<20} {:<30}".format("Game ID", "Team 1", "Team 2", "Game Start Time", "Game End Time"))
    # g.id, t1.player1_id, p1.name, t1.player2_id, p2.name, t2.player1_id, p3.name, t2.player2_id, p4.name, g.game_start_time

    # for game in games:
    #     team1 = get_team(game[0])
    #     team2 = get_team(game[0])
    #     print("{:<10} {:<20} {:<20} {:<20} {:<30}".format(game[0], f"{team1[0][1]}, {team1[1][1]}", f"{team2[0][1]}, {team2[1][1]}", game[4], game[5] # if game[5] else ""))

    while True:
        game_id = input("Enter Game ID to end game (Press 0 to exit): ")

        if game_id == '0':
            print("Exiting now.")
            break

        try:
            game_id = int(game_id)
        except ValueError:
            print_error("Invalid input. Please enter a number.")
            continue

        game = next((g for g in games if g[0] == game_id), None)
        if not game:
            print_error("Invalid Game ID. Please enter a valid Game ID.")
            continue

        team1_score = input("Enter team 1 score: ")
        team2_score = input("Enter team 2 score: ")

        try:
            team1_score = int(team1_score)
            team2_score = int(team2_score)
        except ValueError:
            print_error("Invalid input. Please enter a number.")
            continue

        if team1_score > team2_score:
            winning_team = game[10]
            losing_team = game[11]
        elif team1_score < team2_score:
            winning_team = game[11]
            losing_team = game[10]
        else:
            winning_team = None
            losing_team = None


        game_end_time = datetime.now()

        with get_connection() as conn:
            with get_cursor(conn) as cur:
                try:
                    cur.execute("""UPDATE games
                                    SET team1_score = %s, team2_score = %s, winner_team_id = %s,
                                        game_end_time = %s
                                    WHERE id = %s""",
                                (team1_score, team2_score, winning_team, game_end_time, game_id))

                    if winning_team:
                        for player_id in get_team_player_ids(winning_team):
                            update_player_stats(player_id, 'win')
                        for player_id in get_team_player_ids(losing_team):
                            update_player_stats(player_id, 'lose')
                    else:
                        for player_id in get_team_player_ids(game[2]) + get_team_player_ids(game[3]):
                            update_player_stats(player_id, 'draw')

                except Exception as e:
                    print(f"Error: could not end game: {e}")
                    conn.rollback()
                else:
                    conn.commit()
                    print("Game ended successfully.")
                    break


def get_team(team_id):
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("""SELECT team1.player1_id, player1.name, team1.player2_id, player2.name
                            FROM teams AS team1
                            INNER JOIN players AS player1 ON team1.player1_id = player1.id
                            INNER JOIN players AS player2 ON team1.player2_id = player2.id
                            WHERE team1.id = %s""",
                        (team_id,))
            team1 = cur.fetchall()
            if not team1:
                return None
            
            return team1



def get_team_player_ids(team_id):
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("""SELECT player1_id, player2_id FROM teams WHERE team_id = %s""", (team_id,))
            result = cur.fetchone()
            return result


def update_player_stats(player_id: int, result: str):
    if result not in ['win', 'lose']:
        print_error("Cannot update player stats. Result should be 'win' or 'lose'.")
        return
    
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            try:
                if result == 'win':
                    cur.execute("""UPDATE players
                                    SET played = played + 1, won = won + 1
                                    WHERE id = %s""",
                                (player_id,))
                if result == 'win':
                    cur.execute("""UPDATE players
                                    SET win_percentage = 100 * won / played
                                    WHERE id = %s""",
                                (player_id,))
                elif result == 'lose':
                    cur.execute("""UPDATE players
                                    SET played = played + 1
                                    WHERE id = %s""",
                                (player_id,))
                    cur.execute("""UPDATE players
                                    SET win_percentage = 100 * won / played
                                    WHERE id = %s""",
                                (player_id,))

            except Exception as e:
                print_error(f"Could not update player stats: {e}")
                conn.rollback()
            else:
                conn.commit()
                print(f"Player stats for player id {player_id} updated successfully.")




def get_ongoing_games(session_id):
    with get_connection() as conn:
        with get_cursor(conn) as cur:

            cur.execute("""SELECT 
                                  g.id, t1.player1_id, p1.name, t1.player2_id, p2.name, t2.player1_id, p3.name, t2.player2_id, p4.name, g.game_start_time, g.team1_id , g.team2_id
                           FROM games g
                                  JOIN teams t1 ON g.team1_id = t1.team_id
                                  JOIN players p1 ON p1.id = t1.player1_id
                                  JOIN players p2 ON p2.id = t1.player2_id
                                  JOIN teams t2 ON g.team2_id = t2.team_id
                                  JOIN players p3 ON p3.id = t2.player1_id
                                  JOIN players p4 ON p4.id = t2.player2_id
                            WHERE 
                                  g.session_id = %s AND g.game_end_time IS NULL
                            ORDER BY g.game_start_time;""",
                        (session_id,))
            games = cur.fetchall()

            print_info("Ongoing Games")
            for game in games:
# print("{:<10} {:<20} {:<20} {:<20} {:<30}".format(game[0], f"{team1[0][1]}, {team1[1][1]}", f"{team2[0][1]}, {team2[1][1]}", game[4], game[5]

                print(f"{game[0]}. -- Team 1: {game[2]}, {game[4]} .. VS .. Team 2: {game[6]}, {game[8]} | Start Time: {game[9]}")
            print_seperator_tilda()
            print(" ")
            return games

def report_session_games_played(club_id, session_id):
    pass

def set_options(club_id):
    pass



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
            cur.execute("""SELECT player_name, num_games_played, wins, losses, ROUND(win_percentage,0), minutes_since_last_game, session_rank
                           FROM player_session_stats
                           WHERE club_id = %s AND season_id = %s AND session_id = %s""",
                        (club_id, season_id, session_id,))
            player_stats = cur.fetchall()

            # Print results in tabular format
            print (" ")
            print("\033[4m{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}\033[0m".format(
                "", "", "", "", "", "", ""
            ))
            print("\033[1m{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}\033[0m".format(
                "Player", "Games Played", "Games Won", "Games Lost", "Win Percentage", "Mins, Last Game", "Rank"
            ))
            print("\033[4m{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}\033[0m".format(
                "", "", "", "", "", "", ""
            ))
            for stats in player_stats:
                print("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format(*stats))

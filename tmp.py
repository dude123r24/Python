import psycopg2
import hashlib
import getpass
from datetime import date
import datetime

var_club_id = None
var_season_id = None
var_session_id = None
dict_players_in_club = {}

def display_menu():
    print("Club Session Screen")
    print("1.  Select club and season")
    print("2.  Select players playing")
    print("3.  Start a game")
    print("4.  End a game")
    print("5.  See all games played this session")
    print("6.  See games played per player")
    print("7.  See games played by a player")
    print("8.  Options")
    print("9.  Feedback")
    print("10. Exit")
    user_choice = None
    while user_choice is None:
        try:
            user_choice = int(input("Enter a number: "))
        except ValueError:
            print("Invalid choice. Please enter a valid number.")
        if user_choice == 1:
            select_club_and_season()
        elif user_choice == 2:
            select_session_players()
        elif user_choice == 3:
            select_teams()
        elif user_choice == 4:
            end_game()
        elif user_choice == 5:
            report_session_games_played()
        elif user_choice == 6:
            report_session_all_players_games_played()
        elif user_choice == 7:
            report_session_players_games_played()
        elif user_choice == 8:
            menu_options()
        elif user_choice == 9:
            display_club_owner_details()
        elif user_choice == 10:
            print("Exiting program...")
            exit()
        else:
            print("Invalid choice. Please try again.")
            display_menu()

def connect_to_database():
    conn = psycopg2.connect(
        host="localhost",
        database="badminton",
        user="amitsanghvi",
        password="joy4unme"
    )
    return conn

def hash_password(password):
    # Hash the password for security
    return hashlib.sha256(password.encode()).hexdigest()

def select_club_and_season():
    global var_club_id, var_season_id, dict_players_in_club
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM clubs")
    clubs = cur.fetchall()
    if not clubs:
        print("No clubs found in the database.")
        return
    print("Select a club by entering the club ID:")
    for club in clubs:
        print(f"{club[0]}. {club[1]}")
    club_id = None
    while club_id is None:
        try:
            club_id = int(input("Enter a club ID: "))
            if not any(club[0] == club_id for club in clubs):
                print("Invalid club ID. Please enter a valid ID.")
                club_id = None
        except ValueError:
            print("Invalid club ID. Please enter a valid ID.")
    var_club_id = club_id
    cur.execute("SELECT id, date_from, date_to FROM season WHERE club_id=%s ORDER BY date_from DESC", (club_id,))
    seasons = cur.fetchall()
    if not seasons:
        print("No seasons found for this club in the database.")
        return
    print("Select a season by entering the season ID:")
    for season in seasons:
        print(f"{season[0]}. {season[1].strftime('%Y-%m-%d')} - {season[2].strftime('%Y-%m-%d')}")
    season_id = None
    while season_id is None:
        try:
            season_id = int(input("Enter a season ID: "))
            if not any(season[0] == season_id for season in seasons):
                print("Invalid season ID. Please enter a valid ID.")
                season_id = None
            else:
                var_season_id = season_id
#                dict_players_in_club = get_players_in_club(var_club_id)
                print(f"Club ID {var_club_id} and Season ID {var_season_id} selected.")
                display_menu()
        except ValueError:
            print("Invalid season ID. Please enter a valid ID.")
    cur.close()
    conn.close()

def create_session(var_season_id):
    conn = connect_to_database()
    cur = conn.cursor()

    today = datetime.datetime.now().date()

    cur.execute("SELECT * FROM sessions WHERE season_id=%s AND session_date=%s", (var_season_id, today))
    if cur.fetchone() is None:
        while True:
            try:
                var_no_of_courts = int(input("Enter number of courts (1-10): "))
                if var_no_of_courts < 1 or var_no_of_courts > 10:
                    print("Invalid input. Please enter a number between 1 and 10.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 10.")
                continue
        cur.execute("INSERT INTO sessions (season_id, club_id, session_date, no_of_courts, no_of_players_per_court, players_played) VALUES (%s, %s, %s, %s, %s, '0') RETURNING id", (var_season_id, var_club_id, today, var_no_of_courts, 4))
        
        var_session_id = cur.fetchone()[0]
        conn.commit()
        print(f"Session created with ID {var_session_id} for today's date {today}.")
    else:
        print("A session already exists for today's date.")
        return
    cur.close()
    conn.close()


def select_session_players():
    global var_session_id, dict_players_in_club
    
    conn = connect_to_database()
    cur = conn.cursor()
    
    # Check if there is a session for today
    cur.execute("SELECT id, no_of_courts FROM sessions WHERE season_id=%s AND session_date=%s", (var_season_id, date.today()))
    session_row = cur.fetchone()
    
    if session_row is None:
        create_session(var_season_id)
        cur.execute("SELECT id, no_of_courts FROM sessions WHERE season_id=%s AND session_date=%s", (var_season_id, date.today()))
        session_row = cur.fetchone()
        
    var_session_id, var_no_of_courts = session_row[0], session_row[1]

    # Get list of players who have not played in the session yet
    cur.execute("""
        SELECT pc.player_id, p.name
        FROM players_clubs pc
        JOIN players p ON pc.player_id = p.id
        WHERE pc.club_id = %s
        AND pc.player_id NOT IN (
            SELECT player_id FROM sessions_players_active WHERE session_id = %s
        )
        AND pc.approved = TRUE
        AND pc.archived = FALSE
    """, (var_club_id, var_session_id))
    players = cur.fetchall()

    if not players:
        print("No players available to play in this session.")
        return

    print("Select players to play in this session:")
    print(f"Number of courts available: {var_no_of_courts}")
    print(f"Number of players allowed per court: 4")
    
    # Print list of players
    dict_players_in_club = {player[0]: player[1] for player in players}
    for player in players:
        print(f"{player[0]}. {player[1]}")

    selected_players = set()
    while len(selected_players) < var_no_of_courts * 4:
        try:
            selected_player = int(input(f"Enter player ID ({len(selected_players) + 1}/{var_no_of_courts * 4}): "))
            if selected_player not in dict_players_in_club:
                print("Invalid player ID. Please enter a valid ID.")
            elif selected_player in selected_players:
                print("Player already selected. Please choose a different player.")
            else:
                selected_players.add(selected_player)
        except ValueError:
            print("Invalid player ID. Please enter a valid ID.")

    # Insert selected players into sessions_players_active table
    for player_id in selected_players:
        cur.execute("INSERT INTO sessions_players_active (session_id, player_id) VALUES (%s, %s)", (var_session_id, player_id))
    conn.commit()

    print(f"{len(selected_players)} players selected to play in this session.")
    display_menu()
    cur.close()
    conn.close()


if __name__ == "__main__":
    while True:
        display_menu()
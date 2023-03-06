"""
Write a python and postgresql application to manage a badminton club and facilitate the club to hold club sessions to play games.

At the start of the program display a menu to register, login or see list of clubs.

When a player selects register, allow the player to register themselves in players table.
For the players table, the player password is stored in an encrypted format in the password column. Columns played, won, draw, win_percentage are all updated automatically when the players win or lose a game. Date joined is by default today's date.

When a player has logged in show him a menu to register new club, join a club.
If the player is owner or admin of any club, also show him a menu to create a new season, create a new session, approve membership request.
"""


import psycopg2
import hashlib
import getpass

def hash_password(password):
    # Hash the password for security
    return hashlib.sha256(password.encode()).hexdigest()

def connect_to_database():
    conn = psycopg2.connect(
        host="localhost",
        database="badminton",
        user="amitsanghvi",
        password="joy4unme"
    )
    return conn

def register_player(name, email, phone, password):
    conn = connect_to_database()
    cur = conn.cursor()
    hashed_password = hash_password(password)
    cur.execute("""
        INSERT INTO players (name, email, phone, password)
        VALUES (%s, %s, %s, %s)
        """, (name, email, phone, hashed_password))
    conn.commit()
    cur.close()
    conn.close()
    print("Player registered successfully!")

def login_player(email, password):
    conn = connect_to_database()
    cur = conn.cursor()
    hashed_password = hash_password(password)
    cur.execute("""
        SELECT id FROM players
        WHERE email = %s AND password = %s
        """, (email, hashed_password))
    player_id = cur.fetchone()
    cur.close()
    conn.close()
    if player_id:
        return player_id[0]
    else:
        return None

def register_club(name, created_by):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clubs (name, created_by)
        VALUES (%s, %s)
        """, (name, created_by))
    conn.commit()
    cur.close()
    conn.close()
    print("Club registered successfully!")

def create_season(club_id, date_from, date_to):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO season (club_id, date_from, date_to)
        VALUES (%s, %s, %s)
        """, (club_id, date_from, date_to))
    conn.commit()
    cur.close()
    conn.close()
    print("Season created successfully!")


def create_session(season_id, club_id, date, no_of_courts, no_of_players_per_court):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sessions (season_id, club_id, date, no_of_courts, no_of_players_per_court)
        VALUES (%s, %s, %s, %s, %s)
        """, (season_id, club_id, date, no_of_courts, no_of_players_per_court))
    conn.commit()
    cur.close()
    conn.close()
    print("Session created successfully!")

def approve_membership_request(player_id, club_id):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("""
        UPDATE players_clubs
        SET approved = true
        WHERE player_id = %s AND club_id = %s
        """, (player_id, club_id))
    conn.commit()
    cur.close()
    conn.close()
    print("Membership request approved successfully!")

def join_club(player_id, club_id, role, grade, ranking):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO players_clubs (club_id, player_id, role, grade, ranking)
        VALUES (%s, %s, %s, %s, %s)
        """, (club_id, player_id, role, grade, ranking))
    conn.commit()
    cur.close()
    conn.close()
    print("Joined club successfully!")

def list_clubs():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM clubs
        """)
    clubs = cur.fetchall()
    cur.close()
    conn.close()
    return clubs

def main_menu():
    print("Badminton Club Management System")
    print("1. Register")
    print("2. Login")
    print("3. List Clubs")
    print("4. Exit")
    choice = None
    while choice is None:
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please enter a valid number.")
    if choice == 1:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone: ")
        password = getpass.getpass(prompt="Enter your password: ")
        register_player(name, email, phone, password)
    elif choice == 2:
        email = input("Enter your email: ")
        password = getpass.getpass(prompt="Enter your password: ")
        player_id = login_player(email, password)
        if player_id:
            player_menu(player_id)
        else:
            print("Login failed! Incorrect email or password.")
    elif choice == 3:
        clubs = list_clubs()
        print("List of Clubs:")
        for club in clubs:
            print(club[0], club[1])
    else:
        exit()

def player_menu(player_id):
    print("Badminton Club Management System - Player Menu")
    print("1. Register New Club")
    print("2. Join Club")
    print("3. View Club Memberships")
    print("4. Exit")
    choice = None
    while choice is None:
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please enter a valid number.")
    if choice == 1:
        name = input("Enter club name: ")
        register_club(name, player_id)
        player_menu(player_id)
    elif choice == 2:
        club_id = int(input("Enter club id: "))
        role = input("Enter your role (e.g. Member, Admin, Owner): ")
        grade = input("Enter your grade (e.g. A, B, C): ")
        ranking = int(input("Enter your ranking: "))
        join_club(player_id, club_id, role, grade, ranking)
        player_menu(player_id)
    elif choice == 3:
        club_memberships = view_club_memberships(player_id)
        print("List of Club Memberships:")
        for club_membership in club_memberships:
            print(club_membership[0], club_membership[1], club_membership[2], club_membership[3], club_membership[4], club_membership[5], club_membership[6])
        player_menu(player_id)
    else:
        exit()

def view_club_memberships(player_id):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM players_clubs
        WHERE player_id = %s
        """, (player_id,))
    club_memberships = cur.fetchall()
    cur.close()
    conn.close()
    return club_memberships

if __name__ == "__main__":
    while True:
        main_menu()

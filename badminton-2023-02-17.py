
# For 
def print_seperator_dash():
    print ("--------------------------------------------------")

# For 
def print_seperator_doubledash():
    print ("==================================================")

# For headings
def print_seperator_tilda():
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# For error messages
def print_seperator_star():
    print ("**************************************************")

########################################################################################################
# Function to display menu for anyone logged in
########################################################################################################
def display_menu_logged_in():
    print_seperator_dash()
    print(" ")
    print_seperator_tilda()
    print("Club Session Management")
    print_seperator_tilda()
    print(" ")

    options = ["Select your club and season",
               "Select players playing",
               "End session for player",
               "Start a game",
               "End a game",
               "See all games played this session",
               "See no of games played by each player",
               "See games played by a player",
               "See all club players",
               "Options",
               "Feedback",
               "Exit"]
    
    # Print options
    for i, option in enumerate(options):
        print("{:<4d} {:s}".format(i+1, option))
    print(" ")
    choice = input("Enter your choice: ")
    print_seperator_dash()
    print(" ")

    if not choice.isdigit() or int(choice) not in range(1, len(options)+1):
        print_seperator_star()
        print("---> ERROR: Invalid choice. Please try again.")
        print_seperator_star()
        return 0
    else:
        return int(choice)



########################################################################################################
# Function to accept user input for the menu for anyone logged in
########################################################################################################
def process_menu_logged_in_choice():
    # Accept user input
    while True:
        choice = display_menu_logged_in()

        if choice == 1:
            display_clubs()
            #select_club_and_season()
        elif choice == 2:
            try:
                select_session_players()
            except ValueError as e:
                if str(e) == "Invalid session ID":
                    create_session()
                    select_session_players()
                else:
                    print_seperator_star()
                    print("---> ERROR: " + str(e))
                    print_seperator_star()
        elif choice == 3:
            end_session_players()
        elif choice == 4:
            select_teams()
        elif choice == 5:
            end_game()
        elif choice == 6:
            report_session_games_played()
        elif choice == 7:
            report_session_no_of_games_per_player()
        elif choice == 8:
            report_session_player_games_played()
        elif choice == 9:
            if var_club_id in ['', None]:
                print_seperator_star()
                print ("---> ERROR: Select your club first")
                print_seperator_star()
                process_menu_logged_in_choice()
            else:
                display_club_players(var_club_id)
        elif choice == 10:
            set_options()
        elif choice == 11:
            display_club_owner_details()
        elif choice == 12:
            print("Exiting program...")
            break
#        else:
#            print_seperator_star()
#            print("---> ERROR: Invalid choice. Please try again.")
#            print_seperator_star()


########################################################################################################
# Function to select club and season
########################################################################################################
# Display clubs
def display_clubs():
    global var_club_id
    global var_season_id
    cur = conn.cursor()

    print (" ")
    print_seperator_tilda()
    # Display list of clubs and get user input for club selection
    print("Select your club:")
    print_seperator_tilda()
    cur.execute("SELECT id, name FROM clubs ORDER BY name")
    clubs = cur.fetchall()
    for club in clubs:
        print("{:<4}{:<30}".format(club[0], club[1]))
    print (" ")
    select_club(clubs)
    return clubs

# Select your club
def select_club(clubs):
    global var_club_id
    global var_season_id
    cur = conn.cursor()

    while True:
        try:
            var_club_id_input = input("Enter club ID: ")
            if var_club_id_input in ['', None]:
                print("Club ID cannot be blank. Please try again.")
                continue
            var_club_id = int(var_club_id_input)
            cur.execute("SELECT id FROM clubs WHERE id = %s", (var_club_id,))
            if cur.fetchone() is not None:
                break
            else:
                print("---> ERROR: Invalid club ID. Please try again.")
        except ValueError:
            print_seperator_star()
            print("---> ERROR: Invalid input. Please enter a number.")
            print_seperator_star()
    display_season()

# Display seasons for this club, ordered by latest season first
def display_season():
    global var_club_id
    global var_season_id
    cur = conn.cursor()
    print (" ")
    print_seperator_tilda()
    print("Select your season:")
    print_seperator_tilda()
    cur.execute("SELECT id, date_from, date_to FROM seasons WHERE club_id = %s ORDER BY date_from DESC", (var_club_id,))
    seasons = cur.fetchall()
    for season in seasons:
        print("{:<4}{:<15}{:<15}".format(season[0], season[1].strftime("%Y-%m-%d"), season[2].strftime("%Y-%m-%d")))
    print (" ")
    select_season()
    return var_season_id

# Select your season
def select_season():
    global var_club_id
    global var_season_id
    cur = conn.cursor()
    # Display list of seasons for the selected club and get user input for season selection
    while True:
        try:
            var_season_id_input = input("Enter season ID: ")
            if var_season_id_input in ['', None]:
                print("---> ERROR: Season ID cannot be blank. Please try again.")
                continue
            var_season_id = int(var_season_id_input)
            cur.execute("SELECT id FROM seasons WHERE id = %s AND club_id = %s", (var_season_id, var_club_id))
            if cur.fetchone() is not None:
                break
            else:
                print_seperator_star()
                print("---> ERROR: nvalid season ID. Please try again.")
                print_seperator_star()
        except ValueError:
            print_seperator_star()
            print("---> ERROR: Invalid input. Please enter a number.")
            print_seperator_star()



########################################################################################################
# Function to select teams to play. It also creates a session if not already present
########################################################################################################

# Function to select teams for a game
def select_teams():
    global var_club_id
    global var_season_id
    global var_session_id
    create_session()
    list_players_available = check_session_has_players()
    if list_players_available is None:
        #players_in_club_not_already_playing(var_club_id, var_session_id)
        select_session_players()
    else:
        print("Add code to Select teams")
        time.sleep(2)

# Function to check if there are enough players to players to select 2 teams
def check_session_has_players():
    global var_session_id
    global var_no_of_players_per_court

    if var_no_of_players_per_court is None:
        print_seperator_star()
        print("---> Error: var_no_of_players_per_court is not set.")
        print_seperator_star()
        return None

    cur = conn.cursor()
    cur.execute("SELECT player_id FROM sessions_players_active WHERE session_id = %s", (var_session_id,))
    list_players_available = [row[0] for row in cur.fetchall()]

    no_of_players_available = len(list_players_available) if list_players_available else 0

    if len(list_players_available) >= var_no_of_players_per_court:
        return list_players_available
    else:
        print_seperator_star()
        print(f"---> Error: Number of players available ({len(list_players_available)}) is less than the required number of players per court ({var_no_of_players_per_court})")
        print(f"Info: More players can be added by either ending a game or selecting more players for the session")
        print_seperator_star()
        return None

# Function to select players for a session
def select_session_players():
    global var_session_id

    # Get players not already playing in session
    dict_players_not_already_playing = players_in_club_not_already_playing(var_club_id, var_session_id)

    # Get input from user and validate
    input_str = input("Enter comma separated player IDs to add to session (press enter to go back): ")
    if not input_str:
        return
    input_list = input_str.split(',')
    input_list = [x.strip() for x in input_list]

    list_add_session_players_active = []

    for player_id in input_list:
        player_id=int(player_id) # this line was added as earlier player_id was a str variable. Python does not find str in the key part of dict variable which was int
        if player_id in dict_players_not_already_playing.keys():
            list_add_session_players_active.append(player_id)
        else:
            print_seperator_star()
            print(f"---> ERROR: Invalid input: player with ID {player_id} is not available to add to session")
            print_seperator_star()

    # Add selected players to session
    # dict_add_session_players_active = {var_session_id: list_add_session_players_active}

    # print (f"list_add_session_players_active = {list_add_session_players_active}")
    add_session_players_active(list_add_session_players_active)

    return list_add_session_players_active



def add_session_players_active(list_add_session_players_active):
    global var_session_id
    
    if not list_add_session_players_active:
        print("Error: no players to add to session")
        return

    try:
        cur = conn.cursor()
        for player_id in list_add_session_players_active:
            cur.execute("""INSERT INTO sessions_players_active (session_id, player_id)
                            VALUES (%s, %s)""", (var_session_id, player_id))
        conn.commit()
        print_seperator_dash()
        print(f"{len(list_add_session_players_active)} players added to session")
        print_seperator_dash()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()



# Get a list of players playing in today's session at present
def end_session_players():
    global var_session_id

    # Get players playing in the session
    players_in_session = get_active_players_in_session(var_session_id)

    # Display players in the session
    print("Players in session:")
    for player_id, player_name in players_in_session.items():
        print(f"{player_id}: {player_name}")

    # Get input from user and validate
    input_str = input("Enter comma separated player IDs to remove from session or press enter to go back: ")
    if not input_str:
        return
    input_list = input_str.split(',')
    input_list = [x.strip() for x in input_list]

    list_remove_session_players_active = []

    for player_id in input_list:
        player_id = int(player_id)
        if player_id in players_in_session.keys():
            list_remove_session_players_active.append(player_id)
        else:
            print_seperator_star()
            print(f"---> ERROR: Invalid input: player with ID {player_id} is not active in the session")
            print_seperator_star()

    # Remove selected players from session
    remove_session_players_active(list_remove_session_players_active)

    return list_remove_session_players_active

# Function to remove a player from today's session
def end_session_players():
    global var_session_id

    # Get input from user and validate
    input_str = input("Enter comma separated player IDs to remove from session: ")
    input_list = input_str.split(',')
    input_list = [x.strip() for x in input_list]

    list_remove_session_players_active = []

    dict_players_in_session = get_active_players_in_session(var_session_id)

    print("Players in session:")
    for player_id, player_name in dict_players_in_session.items():
        print(f"{player_id} - {player_name}")

    if len(input_list) == 1 and input_list[0] == "":
        return []

    for player_id in input_list:
        player_id = int(player_id)
        if player_id in dict_players_in_session.keys():
            list_remove_session_players_active.append(player_id)
        else:
            print_seperator_star()
            print(f"---> ERROR: Invalid input: player with ID {player_id} is not active in the session")
            print_seperator_star()

    # Remove selected players from session
    remove_session_players_active(list_remove_session_players_active)

    return list_remove_session_players_active




# Get player id's and player names for players currently playing in today's session
def get_active_players_in_session(session_id):
    cur = conn.cursor()

    # Get the player IDs of players playing in the given session
    cur.execute("SELECT player_id FROM sessions_players_active WHERE session_id = %s", (session_id,))
    rows = cur.fetchall()
    player_ids = [row[0] for row in rows]

    if not player_ids:
        return {}

    # Get the names of players with the retrieved IDs
    cur.execute("SELECT player_id, player_name FROM players WHERE player_id IN %s", (tuple(player_ids),))
    rows = cur.fetchall()
    players = {row[0]: row[1] for row in rows}

    return players




def remove_session_players_active(player_ids):
    global var_session_id

    # Connect to the database
    cur = conn.cursor()

    # Remove selected players from session
    for player_id in player_ids:
        sql = "DELETE FROM sessions_players_active WHERE player_id=%s AND session_id=%s"
        cur.execute(sql, (player_id, var_session_id))

    # Commit changes and close database connection
    conn.commit()
    cur.close()
    conn.close()



# Function to end a game
def end_game():
    global var_club_id
    global var_season_id
    global var_session_id
    # TODO: Implement game ending
    print("End game")

# Function to report all games played in a session
def report_session_games_played():
    global var_club_id
    global var_season_id
    global var_session_id
    # TODO: Implement reporting of games played in a session
    print("Report games played in session")

# Function to report number of games played by each player in a session
def report_session_no_of_games_per_player():
    global var_club_id
    global var_season_id
    global var_session_id
    # TODO: Implement reporting of number of games played by each player in a session
    print("Report number of games played by each player")

# Function to report games played by a specific player in a session
def report_session_player_games_played():
    global var_club_id
    global var_season_id
    global var_session_id
    # TODO: Implement reporting of games played by a specific player in a session
    print("Report games played by player")


# Function to set options
def set_options():
    global var_club_id
    global var_club_name
    global var_season_id
    global var_session_id
    # TODO: Implement setting of options
    print("Set options")

# Function to display club owner details
def display_club_owner_details():
    global var_club_id
    global var_season_id
    global var_session_id
    # TODO: Implement display of club owner details
    print("Display club owner details")

########################################################################################################
# Displays all approved players from the club 
########################################################################################################
def display_club_players(var_club_id):
    if var_club_id is None or not str(var_club_id).isnumeric():
        raise ValueError("Invalid club ID")
    
    cur = conn.cursor()
    cur.execute("""SELECT id, name 
                   FROM players 
                   WHERE id IN (SELECT player_id 
                                FROM players_clubs 
                                WHERE club_id = %s 
                                  AND approved = true 
                                  AND archived = false)
                   ORDER BY id""", (var_club_id,))
    
    dict_players_in_club = {}
    rows = cur.fetchall()
    print (" ")
    print_seperator_tilda()
    print ("Players playing for the club {}".format(var_club_id))
    print_seperator_tilda()

    for row in rows:
        player_id, player_name = row
        print("{:<4}{:<30}".format(player_id, player_name))
        dict_players_in_club[player_id] = player_name
    print (" ")

    return dict_players_in_club


########################################################################################################
# Accepts club and session and returns players from the club that are not already playing in today's session.
# The players already playing go in the table sessions_players_active
########################################################################################################
def players_in_club_not_already_playing(var_club_id, var_session_id):
    if var_club_id is None or not str(var_club_id).isnumeric():
        raise ValueError("Invalid club ID")
    if var_session_id is None or not str(var_session_id).isnumeric():
        raise ValueError("Invalid session ID")
    
    cur = conn.cursor()
    cur.execute("""SELECT id, name 
                   FROM players 
                   WHERE id IN (SELECT player_id 
                                FROM players_clubs 
                                WHERE club_id = %s 
                                  AND approved = true 
                                  AND archived = false)
                     AND id NOT IN (SELECT player_id 
                                    FROM sessions_players_active 
                                    WHERE session_id = %s)""", (var_club_id, var_session_id))
    
    dict_players_not_already_playing = {}
    rows = cur.fetchall()

    print_seperator_tilda()
    for row in rows:
        player_id, player_name = row
        print("{:<4}{:<30}".format(player_id, player_name))
        dict_players_not_already_playing[player_id] = player_name
    print_seperator_tilda()

    return dict_players_not_already_playing


########################################################################################################
# Creates a session 
########################################################################################################
def create_session():
    global var_season_id
    global var_club_id
    global var_session_id
    today = date.today()
    cur = conn.cursor()
    
    # Check season_id is not null and is numeric
    check_season_id()
    
    # Check for existing session for today's date
    var_session_id = check_session_in_progress(var_season_id)

    if var_session_id is not None:
        print("Info: Session for today already in progress with id: {}".format(var_session_id))
        return var_session_id
    
    # Select number of courts and players per court from club_options
    cur.execute("SELECT option_value FROM club_options WHERE club_id = %s AND option_name = 'num_courts'", (var_club_id,))
    row = cur.fetchone()
    if row is None:
        raise ValueError("Could not find value for 'num_courts' in club_options")
    var_no_of_courts = row[0]

    cur.execute("SELECT option_value FROM club_options WHERE club_id = %s AND option_name = 'max_players_per_court'", (var_club_id,))
    row = cur.fetchone()
    if row is None:
        raise ValueError("Could not find value for 'max_players_per_court' in club_options")
    var_no_of_players_per_court = row[0]

    # Call write_create_session to create a new session
    var_session_id = write_create_session(today, var_season_id, var_club_id, var_no_of_courts, var_no_of_players_per_court)

    print("Info: Created session with session id: {}".format(var_session_id))
    return var_session_id

########################################################################################################
# Checks we have a valid season_id 
########################################################################################################
def check_season_id():
    global var_season_id
    
    if var_season_id is None or not str(var_season_id).isnumeric():
        print_seperator_star()
        print("---> Error: Invalid season ID. Please select a season.")
        print_seperator_star()
        display_clubs()
    else:
        cur = conn.cursor()
        cur.execute("SELECT id FROM seasons WHERE id = %s", (var_season_id,))
        row = cur.fetchone()
        if row is None:
            print_seperator_star()
            print("---> Error: Season ID not found. Please select a season.")
            print_seperator_star()
            display_clubs()


########################################################################################################
# Checks if a session is already in progress
########################################################################################################
def check_session_in_progress(season_id):
    check_season_id()
    cur = conn.cursor()
    cur.execute("SELECT id FROM sessions WHERE season_id = %s AND session_date = %s", (season_id, date.today() ) )
    row = cur.fetchone()
    if row is not None:
        global var_no_of_players_per_court
        global var_no_of_courts
        cur = conn.cursor()
        cur.execute("SELECT option_name, option_value FROM club_options WHERE club_id = %s AND option_name IN ('max_players_per_court', 'num_courts')", (var_club_id,))
        options = cur.fetchall()
        for option in options:
            if option[0] == 'max_players_per_court':
                var_no_of_players_per_court = int(option[1])
            elif option[0] == 'num_courts':
                var_no_of_courts = int(option[1])

        # list_last_3_sessions(var_season_id)

        return row[0]
    else:
        return None

########################################################################################################
# Prints last 3 sessions for this season
########################################################################################################
def list_last_3_sessions(var_season_id):
    cur = conn.cursor()
    cur.execute("SELECT id as session_id, club_id, season_id, session_date FROM sessions WHERE season_id = %s ORDER BY session_date DESC LIMIT 3", (var_season_id,))
    rows = cur.fetchall()
    print_seperator_star()
    print("Listing the last 3 sessions for this season:")
    print("")
    for row in rows:
        loop_session_id, loop_club_id, loop_season_id, loop_session_date = row
        print("Session ID: {:<4}, Club ID: {:<4}, Season ID: {:<4}, Session Date: {:<30}".format(loop_session_id, loop_club_id, loop_season_id, loop_session_date.strftime("%Y-%m-%d")))
    print_seperator_star()
    print("")

# Function to write the session details to database
def write_create_session(var_session_date, var_season_id, var_club_id, var_no_of_courts, var_no_of_players_per_court):
    cur = conn.cursor()
    cur.execute("INSERT INTO sessions (season_id, club_id, session_date, no_of_courts, no_of_players_per_court) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (var_season_id, var_club_id, var_session_date, var_no_of_courts, var_no_of_players_per_court))
    conn.commit()
    session_id = cur.fetchone()[0]
    var_session_id = session_id
    return var_session_id





if __name__ == "__main__":


########################################################################################################
# Import modules
#########################################################################################################
    import psycopg2
    import datetime
    import time
    from datetime import date

########################################################################################################
# Connect to database
########################################################################################################
    conn = psycopg2.connect(database="badminton", user="amitsanghvi", password="joy4unme", host="localhost", port="5432")


########################################################################################################
# Define global variables
########################################################################################################
    var_club_id = None
    var_season_id = None
    var_session_id = None
    var_no_of_courts = None
    var_no_of_players_per_court = None
    list_players_available = {}
    dict_players_in_club = {}
    choice = None
    process_menu_logged_in_choice()
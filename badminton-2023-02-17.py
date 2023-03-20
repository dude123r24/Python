"""
# Seperators
def print_seperator_dash():
def print_seperator_doubledash():
def print_seperator_tilda():
def print_seperator_star():

# Menu
def display_menu_logged_in():
def process_menu_logged_in_choice():

# Club
def display_clubs():
def select_club(clubs):

# Season
def display_season():
def select_season():
def check_season_id():

# Session
def display_last_3_sessions(var_season_id):
def create_session():
def write_create_session(var_session_date, var_season_id, var_club_id, var_no_of_courts, var_no_of_players_per_court):
def check_session_in_progress(season_id):
    
# Run a session
def check_session_has_players():
def select_session_players():


def players_in_club_not_already_playing(var_club_id, var_session_id):
def add_session_players_active(list_add_session_players_active):

def players_in_club_already_playing(var_club_id, var_session_id):
def deselect_session_players():
def remove_session_players_active(list_player_ids):
def delete_session_players_active(list_delete_session_players_active):


def select_teams():
def end_game():
def report_session_games_played():
def report_session_no_of_games_per_player():
def report_session_player_games_played():
def set_options():
def display_club_owner_details():
def display_club_players(var_club_id):


"""


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
    #print_seperator_dash()
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
            deselect_session_players()
            #end_session_players()
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
            display_club_players(var_club_id)
        elif choice == 10:
            set_options()
        elif choice == 11:
            display_club_owner_details()
        elif choice == 12:
            print("Exiting program...")
            break


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
        print("{:<4d} {:<30}".format(club[0], club[1]))
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
        print("{:<4d} {:<15}{:<15}".format(season[0], season[1].strftime("%Y-%m-%d"), season[2].strftime("%Y-%m-%d")))
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
# Checks we have a valid season_id 
########################################################################################################
def check_season_id():
    global var_season_id
    
    if var_season_id is None or not str(var_season_id).isnumeric():
        print_seperator_star()
        print("---> ERROR: Invalid season ID. Please select a season.")
        print_seperator_star()
        display_clubs()
    else:
        cur = conn.cursor()
        cur.execute("SELECT id FROM seasons WHERE id = %s", (var_season_id,))
        row = cur.fetchone()
        if row is None:
            print_seperator_star()
            print("---> ERROR: Season ID not found. Please select a season.")
            print_seperator_star()
            display_clubs()


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
        #print (" ")
        #print_seperator_dash()
        #print("Info: Session for today already in progress with id: {}".format(var_session_id))
        #print_seperator_dash()
        #print (" ")
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

    # Write a new session to the sessions table
    try:
        cur.execute("""INSERT INTO sessions (season_id, club_id, session_date, no_of_courts, no_of_players_per_court)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                    (var_season_id, var_club_id, today, var_no_of_courts, var_no_of_players_per_court))
        var_session_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        raise

    print("Info: Created session with session id: {}".format(var_session_id))
    return var_session_id


# Function to write the session details to database
def write_create_session(var_session_date, var_season_id, var_club_id, var_no_of_courts, var_no_of_players_per_court):
    cur = conn.cursor()
    cur.execute("INSERT INTO sessions (season_id, club_id, session_date, no_of_courts, no_of_players_per_court) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (var_season_id, var_club_id, var_session_date, var_no_of_courts, var_no_of_players_per_court))
    conn.commit()
    session_id = cur.fetchone()[0]
    var_session_id = session_id
    return var_session_id


########################################################################################################
# Prints last 3 sessions for this season
########################################################################################################
def display_last_3_sessions(var_season_id):
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

        # display_last_3_sessions(var_season_id)

        return row[0]
    else:
        return None

# Function to check if there are enough players to players to select 2 teams
def check_session_has_players():
    global var_session_id
    global var_no_of_players_per_court

    cur = conn.cursor()
    cur.execute("SELECT player_id FROM sessions_players_active WHERE session_id = %s", (var_session_id,))
    list_players_available = [row[0] for row in cur.fetchall()]

    no_of_players_available = len(list_players_available) if list_players_available else 0

    if len(list_players_available) >= var_no_of_players_per_court:
        return list_players_available
    else:
        print_seperator_star()
        print(f"---> ERROR: Number of players available ({len(list_players_available)}) is less than the required number of players per court ({var_no_of_players_per_court})")
        print(f"Info: More players can be added by either ending a game or selecting more players for the session")
        print_seperator_star()
        return None


# Function to select players to play for a session
def select_session_players():
    global var_session_id, var_club_id

    print_seperator_tilda()
    print("Select Players Playing Today")
    print_seperator_tilda()

    if not var_club_id:
        print_seperator_star()
        print("---> ERROR: club not selected")
        print_seperator_star()
        display_clubs()

    if not var_session_id:
        create_session()

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
        print("{:<4d} {:<30}".format(player_id, player_name))
        dict_players_not_already_playing[player_id] = player_name
    print_seperator_tilda()

    return dict_players_not_already_playing



# Function to write the data for adding players to session 
def add_session_players_active(list_add_session_players_active):
    global var_session_id
    
    if not list_add_session_players_active:
        print("---> ERROR: no players to add to session")
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
        print_seperator_star()
        print(f"---> ERROR: {e}")
        print_seperator_star()
        conn.rollback()
#    finally:
#        cur.close()



########################################################################################################
# Accepts club and session and returns players from the club that are already playing in today's session.
########################################################################################################
def players_in_club_already_playing(var_club_id, var_session_id):
    if var_club_id is None or not str(var_club_id).isnumeric():
        raise ValueError("Invalid club ID")
    if var_session_id is None or not str(var_session_id).isnumeric():
        raise ValueError("Invalid session ID")

    cur = conn.cursor()
    cur.execute("""SELECT sp.player_id, p.name 
                   FROM sessions_players_active sp
                   INNER JOIN players p ON sp.player_id = p.id
                   WHERE sp.session_id = %s""", (var_session_id,))
    
    dict_players_already_playing = {}
    rows = cur.fetchall()

    print_seperator_tilda()
    for row in rows:
        player_id, player_name = row
        print("{:<4d} {:<30}".format(player_id, player_name))
        dict_players_already_playing[player_id] = player_name
    print_seperator_tilda()

    return dict_players_already_playing


# Function to select players to remove from today's session 
def deselect_session_players():
    global var_session_id, var_club_id

    print_seperator_tilda()
    print("End Session For Players")
    print_seperator_tilda()

    if not var_club_id:
        print_seperator_star()
        print("---> ERROR: club not selected")
        print_seperator_star()
        display_clubs()

    if not var_session_id:
        create_session()

    dict_players_in_session = players_in_club_already_playing(var_club_id,var_session_id)

    if not dict_players_in_session:
        print("---> ERROR: no players to remove from session")
        return

    # Get input from user and validate
    input_str = input("Enter comma separated player IDs to remove from session (press enter to go back): ")
    if not input_str:
        return
    input_list = input_str.split(',')
    input_list = [x.strip() for x in input_list]

    list_remove_session_players_active = []

    for player_id in input_list:
        player_id = int(player_id)
        if player_id in dict_players_in_session.keys():
            list_remove_session_players_active.append(player_id)
        else:
            print_seperator_star()
            print(f"---> ERROR: Invalid input: player with ID {player_id} is not available to remove from session")
            print_seperator_star()

    if list_remove_session_players_active:
        # Remove selected players from session
        delete_session_players_active(list_remove_session_players_active)

    return list_remove_session_players_active


def remove_session_players_active(list_player_ids):
    global var_session_id

    # Connect to the database
    cur = conn.cursor()

    # Remove selected players from session
    for player_id in list_player_ids:
        sql = "DELETE FROM sessions_players_active WHERE player_id=%s AND session_id=%s"
        cur.execute(sql, (player_id, var_session_id))

    # Commit changes and close database connection
    conn.commit()


# Function to write the data for deleting players from session 
def delete_session_players_active(list_delete_session_players_active):
    global var_session_id
    
    if not list_delete_session_players_active:
        print_seperator_star()
        print("---> ERROR: no players to delete from session")
        print_seperator_star()
        return

    try:
        cur = conn.cursor()
        for player_id in list_delete_session_players_active:
            cur.execute("""DELETE FROM sessions_players_active 
                            WHERE session_id = %s AND player_id = %s""", (var_session_id, player_id))
        conn.commit()
        print_seperator_dash()
        print(f"{len(list_delete_session_players_active)} players removed from session")
        print_seperator_dash()
    except Exception as e:
        print_seperator_star()
        print(f"---> ERROR: {e}")
        print_seperator_star()
        conn.rollback()
#    finally:
#        cur.close()


########################################################################################################
# Function to select teams to play. It also creates a session if not already present
########################################################################################################
# Function to select teams for a game
def select_teams():
    global var_club_id
    global var_season_id
    global var_session_id
    
    cur = conn.cursor()
    
    print_seperator_tilda()
    print("Start A Game / Create Teams")
    print_seperator_tilda()

    create_session()
    
    # Check if session has enough players, and prompt user to add more players if not
    list_players_available = check_session_has_players()
    if list_players_available is None:
        select_session_players()
        list_players_available = check_session_has_players()
        if list_players_available is None:
            print("Error: Insufficient players in session")
            return
        
    # Get team selection algorithm from club_options table
    cur.execute("SELECT option_value FROM club_options WHERE club_id = %s AND option_name = 'algorithm'", (var_club_id,))
    row = cur.fetchone()
    if row is None:
        print("Error: Could not find value for 'algorithm' in club_options")
        return
    var_algorithm = row[0]
    
    # Select team selection function based on algorithm
    if var_algorithm == "random":
        var_team_function = select_team_random
    elif var_algorithm == "rank":
        var_team_function = select_team_rank
    else:
        print("Error: Invalid value for 'algorithm' in club_options")
        return
    
    # Call team selection function
    teams = var_team_function(var_session_id)
    print("Teams selected:")
    for i, team in enumerate(teams):
        print("Team {}:".format(i+1))
        for player in team:
            print("- {}".format(player[1]))



def select_team_random(var_session_id):
    cur = conn.cursor()

    # Select team players
    cur.execute("""
        SELECT p1.id, p2.id
        FROM (
            SELECT p.id, COALESCE(games_played, 0) AS games_played, latest_game_end_time
            FROM players p
            LEFT JOIN (
                SELECT player1_id AS id, COUNT(*) AS games_played, MAX(game_end_time) AS latest_game_end_time
                FROM games
                JOIN teams ON games.team1_id = teams.team_id OR games.team2_id = teams.team_id
                WHERE games.session_id = %s AND games.game_end_time IS NOT NULL
                GROUP BY player1_id
                UNION ALL
                SELECT player2_id AS id, COUNT(*) AS games_played, MAX(game_end_time) AS latest_game_end_time
                FROM games
                JOIN teams ON games.team1_id = teams.team_id OR games.team2_id = teams.team_id
                WHERE games.session_id = %s AND games.game_end_time IS NOT NULL
                GROUP BY player2_id
            ) g ON p.id = g.id
            WHERE g.games_played = (
                SELECT MIN(games_played)
                FROM (
                    SELECT COALESCE(COUNT(*), 0) AS games_played
                    FROM games
                    JOIN teams ON games.team1_id = teams.team_id OR games.team2_id = teams.team_id
                    WHERE games.session_id = %s AND games.game_end_time IS NOT NULL AND (teams.player1_id = p.id OR teams.player2_id = p.id)
                    GROUP BY teams.player1_id, teams.player2_id
                ) t
            )
            ORDER BY g.games_played, g.latest_game_end_time ASC
            LIMIT 2
        ) p
        ORDER BY RANDOM()
        LIMIT 1;
    """, (var_session_id, var_session_id, var_session_id))
    team_player1_id, team_player2_id = cur.fetchone()

    # Write team to teams table
  #  cur.execute("""
  #      INSERT INTO teams (player1_id, player2_id)
  #      VALUES (%s, %s)
  #      RETURNING team_id;
  #  """, (team_player1_id, team_player2_id))
  #  team_id = cur.fetchone()

    # Write game to games table
  #  cur.execute("""
  #      INSERT INTO games (session_id, team1_id, team2_id, team1_score, team2_score, game_start_time)
  #      VALUES (%s, %s, NULL, 0, 0, %s)
  #      RETURNING id;
  #  """, (var_session_id, team_id, datetime.now()))
  #  var_game_id = cur.fetchone()

    # Commit changes and close connection
  #  conn.commit()

    print(f"Team: {team_player1_id}, {team_player2_id}")

    return var_game_id


def select_team_rank():
    print ("select_team_rank")

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
    if var_club_id is ['', None] or not str(var_club_id).isnumeric():
        print_seperator_star()
        print ("---> ERROR: Select your club first")
        print_seperator_star()
        display_clubs()
                
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
        print("{:<4d} {:<30}".format(player_id, player_name))
        dict_players_in_club[player_id] = player_name
    print (" ")

    return dict_players_in_club





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
    dict_players_not_already_playing = {}
    dict_players_already_playing = {}
    choice = None
    process_menu_logged_in_choice()
# Final program

# Example Usage
# initialize()
# select_players()
# play_finished()
# players_status():

import random
from os import system, name

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def print_divider_plus():
    print ("+++++++++++++++++++++++++++++")
    
def print_divider_star():
    print ("*****************************")

def print_divider_line():
    print ("_____________________________")


def initialize():
    global player_names
    global players_playing
    global players_played

    player_names_list = ['anil','sudheer','pratik','asanghvi','yee','ashah','prashant','sunilt','bipin','pranay','sunilm']

    player_names = [item.lower() for item in player_names_list]
    players_playing = []
    players_played = {}
    print ("Players List Reset")
    players_status()


def select_players():
    try:
        # Check if player_names has at least 4 values
        global player_names
        global players_playing
        global players_played
        if len(player_names) >= 4:

            # Select 2 names at random and add them to the players_playing list
            for i in range(2):
                random_index = random.randint(0, len(player_names) - 1)
                players_playing.append(player_names[random_index])
                player_names.pop(random_index)

                # Update the number of games played for the player
                if players_played.get(players_playing[-1]):
                    players_played[players_playing[-1]] += 1
                else:
                    players_played[players_playing[-1]] = 1

            # Repeat the process one more time
            for i in range(2):
                random_index = random.randint(0, len(player_names) - 1)
                players_playing.append(player_names[random_index])
                player_names.pop(random_index)

                # Update the number of games played for the player
                if players_played.get(players_playing[-1]):
                    players_played[players_playing[-1]] += 1
                else:
                    players_played[players_playing[-1]] = 1

            # Print the first 2 names as team1 and next 2 names as team2
            ###### BUG : always DISPLAYING first 4 PLAYERS ########
            no_of_players_playing=len(players_playing)
            print("Team 1:", players_playing[no_of_players_playing-4], players_playing[no_of_players_playing-3])
            print("Team 2:", players_playing[no_of_players_playing-2], players_playing[no_of_players_playing-1])
        else:
            print("Not enough players to create 2 doubles teams. Select option to finish a game to add more players in the available pool.")
            
    except NameError:
        initialize()
        select_players()


def play_finished():
    try:
        global player_names
        global players_playing

        if len(players_playing) >= 1:

            # Display the players_playing list
            print("Players playing:", players_playing)

            # Accept input for comma separated player names
            finished_players = input("Enter comma separated names of finished players: ")
            finished_players = finished_players.lower()

            # Convert the input string to a list of player names
            finished_players = finished_players.split(',')

            # Remove the finished players from the players_playing list
            for player in finished_players:
                players_playing.remove(player.strip())

            # Add the finished players to the player_names list
            for player in finished_players:
                player_names.append(player.strip())

            # Display the updated lists
            players_status()
        else:
            print ("No players playing at present. Can't execute")
    except NameError:
        initialize()
        play_finished()


def players_status():
    try:
        global player_names
        global players_playing

        print_divider_plus()
        print("Players playing:", players_playing)
        print_divider_line()
        print("Players available:", player_names)
        print_divider_plus()
        print("No of games played:", players_played)
        print_divider_plus()

    except NameError:
        initialize()
        players_status()

def show_options():        
    while True:
      print_divider_star()
      print("""Choose 1
      1. Reset Players/Application
      2. Select Players
      3. Finish a game
      4. Current Status of players""")
      choice = int(input("Please select a number (1, 2, 3, 4) or 0 to exit: "))
      print_divider_star()
      if choice == 0:
        break
      elif choice == 1:
        initialize()
      elif choice == 2:
        select_players()
      elif choice == 3:
        play_finished()
      elif choice == 4:
        players_status()
      else:
        print("Invalid selection. Please try again.")
    print("Exiting the program.")

if __name__ == "__main__":
    try:
        show_options()
    except ValueError:
        print("Invalid selection. Please try again.")
        show_options()

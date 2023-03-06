import random

def setup_games(players, courts):
    # Check if number of players is greater than 3
    if len(players) <= 3:
        print("Error: Number of players must be more than 3.")
        return

    # Check if number of players is divisible by 4
    if len(players) % 4 != 0:
        # Add extra players to the games until number of players is divisible by 4
        extra_players = 4 - len(players) % 4
        players += players[:extra_players]

    # Check if number of courts is sufficient
    num_games = len(players) // 4
    if num_games > courts:
        print("Error: Not enough courts to play all the games.")
        return

    # Shuffle the players list
    random.shuffle(players)

    # Split the players list into groups of 4
    games = [players[i:i+4] for i in range(0, len(players), 4)]

    # Print the game schedule
    for i, game in enumerate(games):
        print("Game", i+1)
        print("Players:", game)

# Read the input from a file
with open("Badminton_games_input.txt") as f:
    players = f.readline().strip().split(',')
    courts = int(f.readline().strip())

# Setup the games
setup_games(players, courts)

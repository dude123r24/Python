# main.py

import os
import sys
from login import login
from clubs import display_clubs, set_club, display_club_owner_details
from seasons import get_season, create_new_season
from sessions import create_session, sessions_players_select, check_session_has_players
from players import display_club_players, display_club_players_not_playing_today, display_club_players_playing_today
from games import select_teams, end_game, set_options
from reports import report_session_no_of_games_per_player, report_session_games_played
from utils import print_seperator_tilda, print_title

def main():
    os.system('clear')

    # Login
    while True:
        print_title ("Login")
        player_id = login()
        if player_id is None:
            choice = input("Press 0 to exit, any other key to try again: ")
            if choice == '0':
                sys.exit()
        else:
            break

    # Set club
    while True:
        display_clubs()
        club_input = input("Enter club ID (Press enter to exit): ")

        if not club_input:
            print("No club selected. Exiting now.")
            sys.exit()

        try:
            club_id = int(club_input)
            club_name = set_club(club_id)
            if not club_name:
                continue  # go back to the start of the loop
        except ValueError:
            print("Invalid club ID. Please enter a valid club ID.")
            continue
        except ClubNotFoundError:
            print("Club not found. Please enter a valid club ID.")
            continue



        # Get active season for club
        season_id = get_season(club_id)

        # Create session
        session_id = create_session(club_id)

        # Show menu
        while True:
            print_title("Menu:")
            print("1. Select/View players playing today")
            print("2. Start game")
            print("3. End game")
            print("4. Report games played in session")
            print("5. Report number of games played by each player")
            print("6. Report games played by a specific player")
            print("7. Set options")
            print("8. Display club owner details")
            print("0. Exit")
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == 1:
                sessions_players_select(club_id, season_id, session_id)
            elif choice == 2:
                select_teams(club_id, season_id, session_id)
            elif choice == 3:
                end_game(club_id, season_id, session_id)
            elif choice == 4:
                report_session_games_played(club_id, session_id)
            elif choice == 5:
                report_session_no_of_games_per_player(club_id, season_id)
            elif choice == 6:
                report_session_player_games_played(club_id, session_id)
            elif choice == 7:
                set_options(club_id)
            elif choice == 8:
                display_club_owner_details(club_id, session_id)
            elif choice == 0:
                sys.exit()
            else:
                print("Invalid choice")

if __name__ == "__main__":
    main()

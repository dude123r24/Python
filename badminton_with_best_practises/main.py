# main.py
import os
from clubs import display_clubs, set_club
from sessions import create_session, sessions_players_select, check_session_has_players
from players import display_club_players
from games import select_teams, end_game, report_session_games_played, report_session_no_of_games_per_player, report_session_player_games_played, set_options, display_club_owner_details
from utils import print_seperator_tilda

def main():
    os.system('clear')

    while True:
        display_clubs()
        club_input = input("Enter club ID (Press enter to exit): ")

        if not club_input:
            print("No club selected. Exiting now.")
            break

        try:
            club_id = int(club_input)
            club_name = set_club(club_id)
        except ValueError:
            print("Invalid club ID. Please enter a valid club ID.")
            continue
        except ClubNotFoundError:
            print("Club not found. Please enter a valid club ID.")
            continue

        session_id = create_session(club_id)
        # players = display_club_players(club_id)

        while True:
            print (" ")
            print_seperator_tilda()
            print("Menu:")
            print("1. Select players playing today")
            print("2. Select teams")
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
                sessions_players_select(club_id, session_id)
            elif choice == 2:
                select_teams(club_id, session_id)
            elif choice == 3:
                end_game()
            elif choice == 4:
                report_session_games_played(club_id, session_id)
            elif choice == 5:
                report_session_no_of_games_per_player(club_id, session_id)
            elif choice == 6:
                report_session_player_games_played(club_id, session_id)
            elif choice == 7:
                set_options(club_id, session_id)
            elif choice == 8:
                display_club_owner_details(club_id, session_id)
            elif choice == 0:
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    main()

import time
import random
import json
from pygame import mixer
import sys

# Constants
RECORDS_FILE = 'records.json'
SOUND_VOLUME = 0.5
MAX_SCORE = 30

# Sound initialization
mixer.init()

# background music and sounds
mixer.music.load('backgroundmusic.mp3')
mixer.music.play()
mixer.music.set_volume(0.2)

dice_sound_enabled = True
tiebreaker_sound_enabled = True
victory_sound_enabled = True
background_music_enabled = True

# Sound settings
def sound_settings():
    global dice_sound_enabled, tiebreaker_sound_enabled, victory_sound_enabled, background_music_enabled
    
    print("\nSOUND SETTINGS")
    print("1) Toggle Dice Roll Sound: ", "ON" if dice_sound_enabled else "OFF")
    print("2) Toggle Tiebreaker Sound: ", "ON" if tiebreaker_sound_enabled else "OFF")
    print("3) Toggle Victory Sound: ", "ON" if victory_sound_enabled else "OFF")
    print("4) Toggle Background Music: ", "ON" if background_music_enabled else "OFF")
    print("5) Back to Main Menu")
    
    while True:
        choice = input("Enter a number (1-5): ")

        if choice == '1':
            dice_sound_enabled = not dice_sound_enabled
            print("Dice Roll Sound is now", "ON" if dice_sound_enabled else "OFF")
        elif choice == '2':
            tiebreaker_sound_enabled = not tiebreaker_sound_enabled
            print("Tiebreaker Sound is now", "ON" if tiebreaker_sound_enabled else "OFF")
        elif choice == '3':
            victory_sound_enabled = not victory_sound_enabled
            print("Victory Sound is now", "ON" if victory_sound_enabled else "OFF")
        elif choice == '4':
            if background_music_enabled:
                mixer.music.pause()
            else:
                mixer.music.unpause()
            background_music_enabled = not background_music_enabled
            print("Background Music is now", "ON" if background_music_enabled else "OFF")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Load and save leaderboard
def load_records():
    try:
        with open(RECORDS_FILE, 'r') as file:
            leaderboard = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # Initialize an empty leaderboard structure if the file is empty or not found
        leaderboard = {'entries': []}
    return leaderboard

# Save records
def save_records(leaderboard, name, round_counter):
    leaderboard['entries'].append({'name': name, 'rounds': round_counter})
    with open(RECORDS_FILE, 'w') as file:
        json.dump(leaderboard, file, indent=2)

# Roll the dice with adjusted odds
def roll_dice():
    outcomes = [1, 2, 3, 4, 5, 6]
    probabilities = [0.1, 0.2, 0.2, 0.2, 0.2, 0.1]
    return random.choices(outcomes, probabilities)[0]

# Display game results
def display_results(name, user_score, pc_score):
    print("########################################")
    print(f"{name} Score: {user_score}")
    print(f"Computer Score: {pc_score}")
    print("########################################\n")

# Determine the winner
def determine_winner(name, user_score, pc_score):
    if user_score > pc_score:
        return f"{name} wins!!\n"
    elif user_score < pc_score:
        return "Computer wins!!\n"
    else:
        handle_tiebreaker()

# Handle rules when a 1 is rolled
def handle_one_rule(name, user_dice, pc_dice, user_score, pc_score):
    if user_dice == 1:
        user_score = 0
        print("You got a 1, back to 0!\n")
    elif pc_dice == 1:
        pc_score = 0
        print("Computer got a 1, you're lucky!\n")

    return user_score, pc_score

# Handle the rule when the score exceeds MAX_SCORE
def handle_max_score_rule(name, score):
    if score > MAX_SCORE:
        score = abs(MAX_SCORE - score)
        print(f"{name} exceeded {MAX_SCORE}, Adjusting to {score}\n")
    return score

# Tiebreaker rule
def handle_tiebreaker(name, user_score, pc_score, round_counter):
    print("It's a tie! Let's go to the tiebreaker!\n")

    if tiebreaker_sound_enabled:
        mixer.Sound('empatesound.mp3').play().set_volume(SOUND_VOLUME)

    while user_score == pc_score:
        user_score = 0
        pc_score = 0
        round_counter += 1  # Increment by 1 per tiebreaker round

        # Last roll
        input("Press 'Enter' to play the Tiebreaker round")

        dice_tie_user = roll_dice()
        user_score += dice_tie_user
        print(f"{name} got {dice_tie_user}")
        dice_tie_pc = roll_dice()
        pc_score += dice_tie_pc
        print(f"Computer got {dice_tie_pc}")

    # Determine the winner
    if pc_score > user_score:
        print("Computer wins!!")
    else:
        print(f"{name} wins!!")

    print(f"Number of rounds played in the tiebreaker: {round_counter}\n")

# Ask if the player wants to play again
def play_again():
    while True:
        response = input("Do you want to play another round? (yes/no): ").lower()
        if response in ["yes", "no"]:
            return response == "yes"
        else:
            print("Invalid input. Please enter 'yes' or 'no'\n")

# Main game loop
def main_game(records):
    while True:  # Add a loop to keep playing as long as the user wants
        round_counter = 0  # Number of rounds

        name = input("\nWhat's your name? ").title()
        print(f"Hello, {name}!\n")

        user_score = 0
        pc_score = 0

        # Dice rolling
        while user_score < MAX_SCORE and pc_score < MAX_SCORE:
            round_counter += 1  # Increment by 1 per round

            key_input = input("Press 'Enter' to roll the dice, 'q' to quit to the main menu\n")

            if key_input.lower() == 'q':
                print("Quitting to the main menu...\n")
                return  # Exit the main_game function and go back to the main menu

            # Play dice sound
            if dice_sound_enabled:
                mixer.Sound('somdados.mp3').play().set_volume(SOUND_VOLUME)

            user_dice = roll_dice()
            user_score += user_dice
            print(f"{name} rolls a {user_dice}")

            pc_dice = roll_dice()
            pc_score += pc_dice
            print(f"Computer rolls a {pc_dice}\n")

            # Apply rules
            user_score, pc_score = handle_one_rule(name, user_dice, pc_dice, user_score, pc_score)
            user_score = handle_max_score_rule(name, user_score)
            pc_score = handle_max_score_rule("Computer", pc_score)

            # Display results
            display_results(name, user_score, pc_score)
            time.sleep(1)  # Wait a bit between rolls

        # Determine the winner
        winner_message = determine_winner(name, user_score, pc_score)
        print(winner_message)

        # Play win sound
        if victory_sound_enabled:
            mixer.Sound('victorysound.mp3').play().set_volume(SOUND_VOLUME)

        # If the player wins, save the record
        if winner_message.startswith(f"{name} wins"):
            save_records(records, name, round_counter)  # Pass the name and round_counter to save_records

        # Display number of rounds played
        print(f"\nTotal number of rounds played: {round_counter}\n")

        # Ask to play again
        if not play_again():
            print("\nBye!")
            time.sleep(3)
            break  # Break out of the game loop if the user doesn't want to play again

# Display the leaderboard
def display_leaderboard():
    leaderboard = load_records()
    if leaderboard:
        print("\nLEADERBOARD:")
        for i, entry in enumerate(sorted(leaderboard['entries'], key=lambda x: x['rounds'])):
            print(f"{i + 1}. {entry['name']} - {entry['rounds']} rounds")
    else:
        print("\nLEADERBOARD is empty.")

# Menu text display function
def menu_text():
    print("\n------THE EASIEST DICE GAME------")
    print("\nMAIN MENU")
    print("1) Play")
    print("2) Leaderboard")
    print("3) Sound Settings")
    print("4) Exit")

# Main menu
def main_menu(records):
    while True:
        menu_text()
        choice = input("Enter a number (1-4): ")

        if choice == '1':
            main_game(records)
        elif choice == '2':
            display_leaderboard()
        elif choice == '3':
            sound_settings()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# Main entry point
if __name__ == "__main__":
    records = load_records()  # Load existing records
    main_menu(records)  # Pass records to the main menu

#melhorias

#gui interface
    
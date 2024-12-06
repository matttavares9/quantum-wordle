import random
from backend import QuantumWordle

file_path = "valid-wordle-words.txt" # Credit: https://github.com/Kinkelin/WordleCompetition/edit/main/data/official/shuffled_real_wordles.txt

def choose_random_word(file_path):
    """ Chooses random word from text file. """

    try:
        with open(file_path, 'r') as file:
            words = file.readlines()
        words = [word.strip() for word in words if word.strip()]
        return random.choice(words) if words else None
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

""" Create game with hidden word. """
hidden_word = choose_random_word(file_path) 
game = QuantumWordle(hidden_word)

""" Gameplay logic. """
status = False
attempts = 0
while(True):
    if attempts == 6:
        print("Game over!")
        break
    else:
        if attempts > 1:
            print(f"{6 - attempts} guesses remaining")
        else:
            print(f"{6 - attempts} guess remaining")
        while True:
            try:
                guess = input("Enter guess: ")
                if len(guess) != 5:
                    raise ValueError("Guess must be 5 letters long!")
                if not guess.isalpha():
                    raise ValueError("Guess must contain only letters!")                
                break
            except ValueError as e:
                print(e)
        guess = guess.upper()
        status = game.guess(guess)    
        if status == True:
            break
    attempts+=1
print(f"Hidden word was {hidden_word}")

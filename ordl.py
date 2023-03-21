import random
from collections import Counter
from termcolor import cprint
from enum import Enum

ALLOWED_LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ")
ALLOWED_WORD_LENGTH = 5
ALLOWED_NUMBER_OF_GUESSES = 8

with open("ord", 'r') as f:
    dictionary = f.read().split(" ")

class LetterStatus(Enum):
    WRONG = 0
    WRONG_PLACE = 1
    CORRECT = 2
    NOT_GUESSED = 3

def print_colored_word(guess:str, result:list[LetterStatus]) -> None:
    for i, char in enumerate(guess):
        if result[i] == LetterStatus.WRONG:
            cprint(char, "white", "on_grey", end='')
        elif result[i] == LetterStatus.WRONG_PLACE:
            cprint(char, "grey", "on_yellow", end='')
        elif result[i] == LetterStatus.CORRECT:
            cprint(char, "grey", "on_green", end='')
        else:
            print(char, end='')

def is_valid_guess(guess:str) -> bool:
    for char in guess:
        if not char in ALLOWED_LETTERS:
            return False
    
    return len(guess) == ALLOWED_WORD_LENGTH 


word = random.choice(dictionary)
attempts = 0
guessed_letters = dict(zip(ALLOWED_LETTERS, [LetterStatus.NOT_GUESSED]*len(ALLOWED_LETTERS)))

print(f"Letters in use: {''.join(ALLOWED_LETTERS)}")
print(f"Please guess a word with {len(word)} letters!")

while True:
    guess = input("").upper()
    if not is_valid_guess(guess):
        print("Invalid guess.")
        continue
    elif not guess in dictionary:
        print("Not a valid word.")
        continue
    attempts += 1
    word_stat = Counter(word)
    results = [LetterStatus.WRONG] * ALLOWED_WORD_LENGTH
    correct_letters = [x==y for (x,y) in zip(word, guess)]

    # Do correct letters (greens) first!
    for i, is_correct in enumerate(correct_letters):
        char = guess[i]
        if is_correct:
            results[i] = LetterStatus.CORRECT
            word_stat[char] -= 1
            guessed_letters[char] = LetterStatus.CORRECT

    # Do wrong placed and wrong letters next
    for i, char in enumerate(guess):
        if results[i] != LetterStatus.CORRECT:
            if word_stat[char] > 0:
                results[i] = LetterStatus.WRONG_PLACE
                word_stat[char] -= 1
                if guessed_letters[char] != LetterStatus.CORRECT:
                    guessed_letters[char] = LetterStatus.WRONG_PLACE
            else:
                results[i] = LetterStatus.WRONG
                if guessed_letters[char] == LetterStatus.NOT_GUESSED:
                    guessed_letters[char] = LetterStatus.WRONG

    print_colored_word(guess, results)
    print('\t', end='')
    print_colored_word("".join(ALLOWED_LETTERS), list(guessed_letters.values()))
    print()

    if guess == word:
        print(f"You made it in {attempts} attempt{'' if attempts == 1 else 's'}!") 
        break
    elif attempts >= ALLOWED_NUMBER_OF_GUESSES:
        print(f"Sorry, you lost. The word was {word}.")
        break  

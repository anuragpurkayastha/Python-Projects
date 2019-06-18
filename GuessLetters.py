# -*- coding: utf-8 -*-
"""
Let’s continue building Hangman. In the game of Hangman, a clue word is given by the program that the player has to guess, letter by letter. The player guesses one letter at a time until the entire word has been guessed. (In the actual game, the player can only guess 6 letters incorrectly before losing).

Let’s say the word the player has to guess is “EVAPORATE”. For this exercise, write the logic that asks a player to guess a letter and displays letters in the clue word that were guessed correctly. For now, let the player guess an infinite number of times until they get the entire word. As a bonus, keep track of the letters the player guessed and display a different message if the player tries to guess that letter again. Remember to stop the game when all the letters have been guessed correctly! Don’t worry about choosing a word randomly or keeping track of the number of guesses the player has remaining - we will deal with those in a future exercise.

An example interaction can look like this:

>>> Welcome to Hangman!
_ _ _ _ _ _ _ _ _
>>> Guess your letter: S
Incorrect!
>>> Guess your letter: E
E _ _ _ _ _ _ _ E
...
And so on, until the player gets the word.
"""
from time import sleep

def findLetterIndices(letter,word):
	"""
	This function returns the indices at which 'letter' appears in 'word'. The function returns a LIST of indices.
	'letter' and 'word' are strings.
	"""
	indices = []	# List of indices
	
	# Loop through the word
	for index, character in enumerate(word):
	
		# If the 'letter' is equal to the current character in the word, add the index to the indices list.
		if letter == character:
			indices.append(index)
	
	return indices

# WELCOME MESSAGE
print ("Welcome to HANGMAN!\n")
print ("In this game, you will guess the letters of the random word!\n")

# Word to guess
word = "EVAPORATE"

letters = ["-"]*len(word)	# String as a list to keep track of which letters of the word have been guessed
lettersGuessed = set()			# Keep track of the letters that the user has guessed

# Keep looping until the user guesses the word
while True:
	
	print ("Status: "," ".join(letters),"\n")	# "- - - - - - -" representing the letters of the word

	# If the user has guessed all the letters, print a message and quit.
	if "-" not in letters:
		print ("Congratulations! You have correctly guessed the word!")
		print ("The game will now close...\n")
		sleep(1)
		break
		
	# Ask the user for a guess
	userGuess = str(input("Please enter a letter: ")).upper()
	
	# If the user input is not a letter -> error message.
	if not userGuess.isalpha():
		print ("Oops! That is not a letter. Please try again!")
	# If the user enters more than one letter -> error message
	elif len(userGuess) > 1:
		print ("Oops! You entered more than 1 letter. Please try again!")
	# If the user enters a letter he or she has already guessed -> error message
	elif userGuess.upper() in lettersGuessed:
		print ("You have already guessed that letter! Please try again!")
	else:
		# Add the letter to the list of letters the user has already guessed
		lettersGuessed.add(userGuess.upper())
		
		# If the user's guess is in the word, replace the corresponding indices of 'letters' to the letter input by the user.
		if userGuess.upper() in word:
			
			# Find the indices at which the letter occurs
			letterIndices = findLetterIndices(userGuess,word)
			
			# Loop through the 'letterIndices' list and change the corresponding indices of 'letters' from "-" to the letter.
			for i in letterIndices:
				letters[i] = userGuess.upper()
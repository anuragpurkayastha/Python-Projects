# -*- coding: utf-8 -*-
"""
In this exercise, we will finish building Hangman. In the game of Hangman, the player only has 6 incorrect guesses (head, body, 2 legs, and 2 arms) before they lose the game.

In Part 1, we loaded a random word list and picked a word from it. In Part 2, we wrote the logic for guessing the letter and displaying that information to the user. In this exercise, we have to put it all together and add logic for handling guesses.

Copy your code from Parts 1 and 2 into a new file as a starting point. Now add the following features:

Only let the user guess 6 times, and tell the user how many guesses they have left.
Keep track of the letters the user guessed. If the user guesses a letter they already guessed, don’t penalize them - let them guess again.
"""
from time import sleep
from random import choice

# Import the file containing all the words to be used and assign them in a list.
with open('sowpods.txt','r') as file:
	words = list(file)

def resetGame():
	"""
	This function resets all the variables (random word, letters guessed, number of guesses left)
	"""
	global word
	global guessesLeft
	global letters
	global lettersGuessed
	
	word = pickRandomWord(words)	# Random word to guess
	guessesLeft = 6					# Number of guesses the user has left
	letters = ["-"]*len(word)		# String as a list to keep track of which letters of the word have been guessed
	lettersGuessed = set()			# Keep track of the letters that the user has guessed
	
def restartGame():
	"""
	This function indicates if the user wants to restart or quit the game according to the userReponse (either "yes" or "no"). Returns TRUE if the user wants to restart the game and False if no.
	"""
	# decisionMade = False	# Has a final decision been made?
	
	# Ask the user if they would like to restart. Keep looping until user enters a valid response
	while True:

		userResponse = str(input("Would you like to restart the game (yes/no)? ")).lower()
		
		# If the user wants to restart the game, reset variables.
		if userResponse == "yes":
			print ("Game will restart...\n")
			resetGame()
			return True
		# Else if the user says "no", print message and quit.
		elif userResponse == "no":
			print ("Thanks for playing! Game will now close...\n")
			return False
		else:
			print ("Invalid response. Please try again!\n")
			

def pickRandomWord(wordList):
	"""
	This function picks a random word from the wordList and returns it.
	"""
	return choice(wordList).strip()

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

if __name__ == "__main__":
	# WELCOME MESSAGE
	print ("Welcome to HANGMAN!\n")
	print ("In this game, you will guess the letters of the random word!\n")

	# Initialise game
	resetGame()

	# Keep looping until the user guesses the word
	while True:
		
		# If the user has guessed all the letters, print a message and quit.
		# Else if the user has run out of guesses, print a message and quit.
		if "-" not in letters:
			print ("Congratulations! You have correctly guessed the word '",word.upper(),"'!\n")
			
			# Restart the game?
			if not restartGame():
				sleep(1)
				break
				
		elif guessesLeft == 0:
			print ("You have run out of guesses! The word was, ",word,"\n")

			# Restart the game?
			if not restartGame():
				sleep(1)
				break

		print ("Status: "," ".join(letters))	# "- - - - - - -" representing the letters of the word
		print ("Guesses left: ", guessesLeft,"\n")
		
		# Ask the user for a guess
		userGuess = str(input("Please enter a letter: ")).upper()
		
		# If the user input is not a letter -> error message.
		if not userGuess.isalpha():
			print ("Oops! That is not a letter. Please try again!")
		# If the user enters more than one letter -> error message
		elif len(userGuess) > 1:
			print ("Oops! You entered more than 1 letter. Please try again!")
		# If the user enters a letter he or she has already guessed -> error message
		elif userGuess in lettersGuessed:
			print ("You have already guessed that letter! Please try again!\n")
		else:
			# Add the letter to the list of letters the user has already guessed
			lettersGuessed.add(userGuess)
			
			# If the user's guess is in the word, replace the corresponding indices of 'letters' to the letter input by the user.
			if userGuess in word:
				
				# Find the indices at which the letter occurs
				letterIndices = findLetterIndices(userGuess,word)
				
				# Loop through the 'letterIndices' list and change the corresponding indices of 'letters' from "-" to the letter.
				for i in letterIndices:
					letters[i] = userGuess
			# Else if the user's guess is not in the word, deduct a guess.
			else:
				guessesLeft -= 1

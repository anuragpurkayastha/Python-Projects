"""This time, we’re going to do exactly the opposite. You, the user, will have in your head a number between 0 and 100. The program will guess a number, and you, the user, will say whether it is too high, too low, or your number.

At the end of this exchange, your program should print out how many guesses it took to get your number.

As the writer of this program, you will have to choose how your program will strategically guess.

STRATEGY:
	1. Guess 50.
	2. If too high -> guess 25
		2a. If too low, guess halfway between 25 and 50
		2b. If too high, guess halfway between 0 and 25 etc...

Use the binary search procedure as suggested on https://en.wikipedia.org/wiki/Binary_search_algorithm#Procedure.
"""
from math import floor

# WELCOME MESSAGE
print ("\nWelcome to Guessing Game Two! In this game, pick a number between 0 and 100 (inclusive) and indicate to the computer if the computer's guess is 'too high', 'too low' or 'hit'.\n")
numberFound = False # is the number found?

rangeOfNumbers = range(0,101)
minGuessIndex = 0 # The left most guess index
maxGuessIndex = len(rangeOfNumbers) - 1 # The rightmost guess index
guessCount = 0 # keep track of the number of guesses

# Keep looping while the number is NOT found. (numberFound = False)
while not numberFound:

	m = floor((minGuessIndex + maxGuessIndex) / 2)
	computerGuess = rangeOfNumbers[m]
	guessCount += 1
	
	print ("Computer guess: ", computerGuess) # Print the current computer guess
	userInput = str(input("Is this 'too high', 'too low', or 'hit'? "))
	print ("")
	if userInput == 'too high':
		maxGuessIndex = m - 1
	elif userInput == 'too low':
		minGuessIndex = m + 1
	elif userInput == 'hit':
		numberFound = True
		print (computerGuess, " is your number! This took ",guessCount," guesses!\n")
	else:
		numberFound = True
		print ("Number not found!")
	
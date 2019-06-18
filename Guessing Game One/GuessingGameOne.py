"""Generate a random number between 1 and 9 (including 1 and 9). Ask the user to guess the number, then tell them whether they guessed too low, too high, or exactly right."""
from random import randint
from time import sleep

# Initialise a variable to determine if game still running
gameIsRunning = True

# Generate a random number
randomNum = randint(1,9)

# While the game is running loop continuously.
while gameIsRunning:

	#Ask for user guess
	guess = raw_input("Enter guess (exit to quit): ")
	
	if guess.lower() == "exit":
		# Quit
		print ("Game closing!")
		sleep(2)
		gameIsRunning = False
	elif int(guess) > randomNum:
		#Guess is too high
		print ("Guess is too high!\n")
	elif int(guess) < randomNum:
		#Guess too low
		print ("Guess is too low!\n")
	else:
		#Guess is right
		print ("Guess is right! You win!\n")
		gameIsRunning = False
		
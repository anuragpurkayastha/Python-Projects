"""Write a program (using functions!) that asks the user for a long string containing multiple words. Print back to the user the same string, except with the words in backwards order. For example, say I type the string:

  My name is Michele
Then I would see the string:

  Michele is name My
shown back to me."""

def reverse_word_order(string):
	""" Function reverses the word order of the input 'string' and returns the result"""

	stringSplit = string.split() # Split the string using whitespace as the delimiter

	reversed = stringSplit[::-1] # Reversed the word order of the string

	return " ".join(reversed)

# Ask the user for input string
inputString = input("Please enter a multiple word sentence to be reversed: ")
# Reverse the string and print out the result
print ("The reversed string is: ",reverse_word_order(inputString),"\n")

"""Ask the user for a number and determine whether the number is prime or not. (For those who have forgotten, a prime number is a number that has no divisors.)."""
from time import sleep

def get_user_input():
	""" Function to get the user input"""
	# Ask for user input and return it
	return int(input("Enter a value ('EXIT' to exit): "))

def check_primality(number):
	""" Check if 'number' is a prime number"""
	# If the number is less than  2, the number is not prime. Otherwise loop through all the numbers (x) from 2 to (number - 1) and determine if there are any numbers for which number % x == 0. If there is return and print "It is a prime number!"
	if number < 2:
		return "It is not a prime number!"
	else:
		for num in range(2,number):
			if number % num == 0:
				return "It is a not prime number!"
		return "It is a prime number!"	

print check_primality(get_user_input())
print ("")
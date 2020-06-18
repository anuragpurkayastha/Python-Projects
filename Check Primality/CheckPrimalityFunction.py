"""
	Ask the user for a number and determine whether the number is prime or not. (For those who have forgotten, a prime number is a number that has no divisors.).
"""
def is_prime(number):
	""" Check if 'number' is a prime number"""
	# If the number is less than  2, the number is not prime. Otherwise loop through all the numbers from 2 to (number - 1) and determine if there are any numbers for which number % x == 0. If there is return and print "It is a prime number!"
	if number < 2:
		return False

	for num in range(2,number):
		if number % num == 0:
			return False

	return True

userNumber = int(input('Please enter a number: '))

if is_prime(userNumber):
	print('It is a prime number!')
else:
	print('It is not a prime number!')

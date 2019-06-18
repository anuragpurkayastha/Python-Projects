# Ask for the number
userInput = input("Please enter a number: ")

# Create a list of all the divisors and print it
print (list(x for x in range(1,userInput+1) if userInput % x ==0))
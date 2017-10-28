#Reversing rolls for the computer for teh guess number game

import random

def print_header():
    print("Pick a number for me to guess between 1 and 100\n")
    print("Let me guess a number now\n")
    print("When I guess, type 'l' for lower, 'h' for higher and 'c' for correct\n")

def print_footer(numGuesses, realNum):
    print("I guess your number which was: ", realNum, "\n")
    print("It took me ", numGuesses, " tries!")

def main(): 

    print_header()

    guess = random.randint(1, 100)

    tries = 1 

    response = 'a'
    lowerBound = 1
    upperBound = 100


    while response != 'c':
        print("\nI guess that the number is: ", guess, "\n")
        print("\nAm I correct?\n")
        response = input("Enter answer here: ")

        if response == 'h':
            lowerBound = guess
            guess = random.randint(lowerBound, upperBound)
     
            
        elif response == 'l':
            upperBound = guess
            guess = random.randint(lowerBound, upperBound)

        tries += 1

    print_footer(tries, guess)

    
if __name__ == "__main__":
    main()

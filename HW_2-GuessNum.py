

def print_header():
    print("Pick a number for me to guess between 1 and 100\n")
    print("Let me guess a number now\n")
    print("When I guess, type 'l' for lower, 'h' for higher and 'c' for correct\n")

def print_footer(numGuesses, realNum):
    print("I guess your number which was: ", realNum, "\n")
    print("It took me ", numGuesses, " tries!")

def main(): 

    print_header()
    response = 'x'
    guess = 50
    lower = 1
    upper = 100
    tries = 0 
    
    while response != 'c':
        print("\nI guess that the number is: ", guess, "\n")
        print("\nAm I correct?\n")
        response = input("Enter answer here: ")

        if response == 'h':
            lower = guess
            guess = (guess + upper) // 2
            
            
        elif response == 'l':
            upper = guess
            guess = (guess + lower) // 2

        tries += 1

    print_footer(tries, guess)

    
if __name__ == "__main__":
    main()

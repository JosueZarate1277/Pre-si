import random

x = random.randint(0,50)
guess = None

while (guess is None):
    try: #Checks for any error
        guess = int(input("Guess the number: "))
        if (guess < x):
            print("The number is greater than your guess. Try again")
            guess = None
        elif (guess > x):
            print("The number is smaller than your guess. Try again")
            guess = None
        else:
            print("You got it! The number is ", x)
            break
    except: #Execute if there's a non-valid character
        guess = None
        print("Non-valid value. Try again")
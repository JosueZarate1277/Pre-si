size = float(input("Type the screw size in cm: "))

if (size >= 1 and size < 3):
    print("Your screw's size is SMALL")
elif (size >= 3 and size < 5):
    print("Your screw's size is MEDIUM")
elif (size >= 5 and size < 6.5):
    print("Your screw's size is LARGE")
elif (size >= 6.5 and size < 8.5):
    print("Your screw's size is VERY LARGE")
else:
    print("Your screw's size is not included on our list")
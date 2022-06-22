time = int(input("Insert the time in seconds: "))

days = time//86400 #Seconds in a day
temp = time%86400

hours = temp//3600
temp = temp%3600

minutes = temp//60
temp = temp%60

print("The time converted is ",days," days, ",hours," hours, ",minutes," minutes and ",temp," seconds")
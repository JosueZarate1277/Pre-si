numbers = list()

a = numbers.append(float(input("Insert the first value: ")))
b = numbers.append(float(input("Insert the second value: ")))
c = numbers.append(float(input("Insert the third value: ")))

max = max(numbers)
min = min(numbers)

print("The greatest number is: ", max," and the lowest is: ", min)
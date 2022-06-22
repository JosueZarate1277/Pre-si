fname = None
count = 0
countword = 0

print("Letter Counter")

while fname is None:
    try:
        fname = open(input("Type the name of the file: "))
    except:
        fname = None
        print("File not found")

for line in fname:
    lines = line.split() #Splits text into lines
    for word in lines:
        words = word.split()
        countword = countword+1
        for letter in words:
            letters = list(letter)
            for char in letters:
                if char == 'e':
                    count = count+1
                    break

percent = (count/countword)*100

print("This file contains ",countword, "words, of which ", count," (",percent,"%) contain the letter e")

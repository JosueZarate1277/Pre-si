import re

word = "C:/Users/PC/Documents/Intel/Verificacion Pre-Silicio Primavera 2022/Python/mbox.txt"
file = open (word,'r')

countline = 0
patterns = input("Type the regular expression you want to search: ")         #Define characters to find on the text
for line in file:
    if re.search(patterns, line):  
        countline = countline+1

print("mbox.txt has ", countline, " lines that match with ", patterns)
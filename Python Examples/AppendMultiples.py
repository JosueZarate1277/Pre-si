import os  #Library used to create files if they do not exist

#Syntax: file = open("/route/filename.txt", "w")

word = "C:/Users/PC/Documents/Intel/Verificacion Pre-Silicio Primavera 2022/Python/multiples.txt"
file = open (word,'r')

for line in file:
    lines = line.split() #Splits text into lines
    for string in lines:
       pass
last_num = int(string)

file = open (word,'a')

list = [n for n in range(last_num+5, last_num+55) if n % 5 == 0]
for x in list:
    file.write("\n")
    file.write(str(x))
file.close()
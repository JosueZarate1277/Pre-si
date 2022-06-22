import os  #Library used to create files if they do not exist

#Syntax: file = open("/route/filename.txt", "w")

word = "C:/Users/PC/Documents/Intel/Verificacion Pre-Silicio Primavera 2022/Python/multiples.txt"
f = open (word,'w')
#word = " ".join(([n for n in range(1, 101) if n % 5 == 0]))
list = [n for n in range(1, 55) if n % 5 == 0]
f.write("Multiples of 5:\n")
for x in list:
    f.write("\n")
    f.write(str(x))
f.close()

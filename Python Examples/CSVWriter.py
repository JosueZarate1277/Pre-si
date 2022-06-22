import csv

myData = [["Name", "Grade & Group", "Final Score"],
          ['Alex', 'Brian', '8.5'],
          ['Tom', 'Smith', '9.7'],
          ['Jim', 'Rings', '5.7'],
          ['Paul', 'Moore', '7.8'],
          ['Edward', 'Toomes', '9']]
 
myFile = open('Grades.csv', 'w', newline="")
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)
     
print("Writing complete")
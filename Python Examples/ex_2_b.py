a = int(input("Enter value of a: "))
b = int(input("Enter value of b: "))
if a!=0:
    x=-b/a
    print("The solution for x is ",x)
elif a==0 and b!=0:
    print("x has no solution")
else:
    print("x has infinite solutions")

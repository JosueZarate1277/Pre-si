primes = list()

for x in range(2,101):
    count = 0
    for n in range(1,x+1):
        div = x%n
        if (div == 0):
            count += 1
    if (count==2):
        primes.append(x)

print ("The prime numbers between 1 and 100 are: ", primes)

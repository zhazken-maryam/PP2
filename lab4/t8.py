import math

def prime(n):
    for num in range(2, n + 1):
        isprime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                isprime = False
                break
        if isprime:
            yield num

n = int(input())

for p in prime(n):
    print(p, end=" ")
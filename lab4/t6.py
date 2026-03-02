def fib(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b

n = int(input())

for f in fib(n):
    if f != 0:
        print(",", end="")
    print(f, end="")
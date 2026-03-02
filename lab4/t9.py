def poww(n):
    for i in range(n + 1):
        yield 2 ** i

n = int(input())

for p in poww(n):
    print(p, end=" ")
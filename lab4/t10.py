def lim(a, k):
    yield a * k

a = input().split()
k = int(input())

for i in lim(a, k):
    print(*i)
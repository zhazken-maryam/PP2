n = int(input())
total = {}

for _ in range(n):
    parts = input().split()
    name = parts[0]
    k = int(parts[1])

    if name in total:
        total[name] += k
    else:
        total[name] = k

for name in sorted(total):
    print(name, total[name])

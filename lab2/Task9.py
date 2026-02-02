n = int(input())
arr = list(map(int, input().split()))
max_v = arr[0]
min_v = arr[0]

for i in range(0, len(arr)):
    if arr[i] > max_v:
        max_v = arr[i]
    if arr[i] < min_v:
        min_v = arr[i]

for i in range(0, len(arr)):
    if arr[i] == max_v:
        arr[i] = min_v

print(*arr)

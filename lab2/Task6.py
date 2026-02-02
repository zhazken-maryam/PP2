n = int(input())
arr = list(map(int, input().split()))

max = arr[0]
for i in range(1, len(arr)):
    if arr[i] > max:
        max = arr[i]
print(max)

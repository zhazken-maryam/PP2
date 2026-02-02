n = int(input())
arr = list(map(int, input().split()))

max_el = arr[0]
for i in range(1, len(arr)):
    if arr[i] > max_el:
        max_el = arr[i]
print(max_el)

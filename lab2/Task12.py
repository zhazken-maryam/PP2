n = int(input())
arr = list(map(int, input().split()))

for i in range(0, len(arr)):
    print(arr[i]**2, end = " ")
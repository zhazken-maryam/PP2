
n = int(input())
arr = []

for i in range(0, n+1):
    if i % 12 == 0:
        arr.append(str(i))
        
print(" ".join(arr))
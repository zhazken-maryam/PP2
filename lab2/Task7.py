n = int(input())
arr = list(map(int, input().split()))
max_i=0
max_num = arr[max_i] 

for i in range(0, len(arr)): 
    if max_num < arr[i]: 
        max_num = arr[i] 
        max_i=i
print(max_i+1)
n = int(input())
nums = input().split()
pos = 0
for num in nums:
    if int(num) > 0:
        pos+=1
print(pos)
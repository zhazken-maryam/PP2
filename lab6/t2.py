n = int(input())
nums = list(map(int, input().split()))
even = 0
for x in list(filter(lambda x: x%2==0, nums)):
    even+=1
print(even)


'''
n = int(input())
nums = list(map(int, input().split()))
print(len(list(filter(lambda x: x%2==0,nums))))
'''
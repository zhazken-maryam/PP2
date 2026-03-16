n = int(input())
nums = map(int,input().split())
print(sum(map(lambda x: x**2, nums)))
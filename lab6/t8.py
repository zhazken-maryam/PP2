n = int(input())
nums = list(map(int,input().split()))
nums = set(nums)
print(*sorted(nums))
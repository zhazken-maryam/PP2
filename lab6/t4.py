n = int(input())
l1 = list(map(int, input().split()))
l2 = list(map(int,input().split()))
s = 0
for i,j in zip(l1,l2):
    s+=i*j
print(s)
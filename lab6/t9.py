n = int(input())
l1= input().split()
l2 = list(map(int,input().split()))
a = input()
for x,y in zip(l1,l2):
    if a == x:
        print(y)
        break
else:
    print("Not found")
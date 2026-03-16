import re
t1 = input()
t2 = input()
count = 0
for x in re.findall(t2,t1):
    count+=1
print(count)
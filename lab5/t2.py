import re
t1,t2 = input(), input()
if re.search(t2,t1):
    print("Yes")
else: print("No")
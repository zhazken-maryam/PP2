import re
s,p,r = input(), input(), input()
rep = re.sub(p,r,s)
print(rep)
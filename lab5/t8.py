import re

s = input()
d = input()

eee = re.split(d, s)
print(*eee, sep=",")
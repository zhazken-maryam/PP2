import re
n = input()
a = re.findall(r"\d", n)  #\d only digits
print(*a)

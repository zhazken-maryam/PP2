import re
n = input()
da = re.search(r"\S+@\S+\.\S+", n)
if da: print(da.group())   #вывести найденный кусок
else: print("Not found")
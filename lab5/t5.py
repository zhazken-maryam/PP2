import re
t = input()
if re.match(r'^[a-zA-Z].*\d$',t):
    print("Yes")
else:
    print("No")



    
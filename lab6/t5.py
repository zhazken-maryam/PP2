t = input()
if any(x in "aeiouAEIOU" for x in t):
    print("Yes")
else:
    print("No")
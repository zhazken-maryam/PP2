first_name, last_name, middle_name = input(), input(), input()
for j in range(0, len(last_name)-(len(last_name)-1)):
    a = last_name[0]
for i in range(0, len(first_name)-(len(first_name)-1)):
    b = first_name[0]
for z in range(0, len(middle_name)-(len(middle_name)-1)):
    c = middle_name[0]

letters = []
letters.append(a)
letters.append(b)
letters.append(c)
print("".join(letters))
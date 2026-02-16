# convert letters to digits
d = {
    "ZER":"0","ONE":"1","TWO":"2","THR":"3","FOU":"4",
    "FIV":"5","SIX":"6","SEV":"7","EIG":"8","NIN":"9"
}

# reverse dictionary
r = {v:k for k,v in d.items()}

s = input()

# find operator
if "+" in s:
    op = "+"
elif "-" in s:
    op = "-"
else:
    op = "*"

a, b = s.split(op)

# function to convert
def to_num(x):
    res = ""
    for i in range(0, len(x), 3):
        res += d[x[i:i+3]]
    return int(res)

# calculate
res = eval(str(to_num(a)) + op + str(to_num(b)))

# convert back
out = ""
for digit in str(res):
    out += r[digit]

print(out)

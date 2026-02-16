# dictionary: letters -> digit
d = {
    "ZER":"0","ONE":"1","TWO":"2","THR":"3","FOU":"4",
    "FIV":"5","SIX":"6","SEV":"7","EIG":"8","NIN":"9"
}

# dictionary: digit -> letters
r = {v:k for k,v in d.items()}

s = input()   # get input

# find operator
if "+" in s:
    op = "+"
elif "-" in s:
    op = "-"
else:
    op = "*"

a, b = s.split(op)   # split into two numbers


# convert letters to integer
def to_int(x):
    num = ""
    for i in range(0, len(x), 3):
        num += d[x[i:i+3]]
    return int(num)


n1 = to_int(a)   # first number
n2 = to_int(b)   # second number


# calculate result
if op == "+":
    res = n1 + n2
elif op == "-":
    res = n1 - n2
else:
    res = n1 * n2


# convert result back to letters
ans = ""
for digit in str(res):
    ans += r[digit]

print(ans)   # print answer

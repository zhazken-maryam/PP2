import re

s = input()

def double_digit(m):
    return m.group() * 2

print(re.sub(r'\d', double_digit, s))
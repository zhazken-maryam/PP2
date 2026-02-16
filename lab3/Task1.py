num = input()
for digit in num:
    if int(digit) % 2 != 0:
        print("Not valid")
        break
else:
    print("Valid")
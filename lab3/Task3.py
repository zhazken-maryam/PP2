words = {
"ZERO":"0","ONE":"1","TWO":"2","THREE":"3","FOUR":"4",
"FIVE":"5","SIX":"6","SEVEN":"7","EIGHT":"8","NINE":"9"
}

s = input()

for w in words:
    s = s.replace(w, words[w])

result = str(eval(s))

rev = {v:k for k,v in words.items()}

answer = ""
for digit in result:
    answer += rev[digit]

print(answer)

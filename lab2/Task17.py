n = int(input())
cnt = {}

for _ in range(n):
    phone = input().strip()
    if phone in cnt:
        cnt[phone] += 1
    else:
        cnt[phone] = 1

ans = 0
for phone in cnt:
    if cnt[phone] == 3:
        ans += 1

print(ans)

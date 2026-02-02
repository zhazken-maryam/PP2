n = int(input())
arr = list(map(int, input().split()))

cnt = {}
for x in arr:
    if x in cnt:
        cnt[x] += 1
    else:
        cnt[x] = 1

best_num = arr[0]
best_count = cnt[best_num]

for x in cnt:
    if cnt[x] > best_count:
        best_count = cnt[x]
        best_num = x
    elif cnt[x] == best_count and x < best_num:
        best_num = x

print(best_num)

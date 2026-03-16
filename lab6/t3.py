n = int(input())
text = input().split()
for i, w in enumerate(text):
    print(f"{i}:{w}", end = " ")
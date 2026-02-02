import sys

data = sys.stdin.read().splitlines()
n = int(data[0])

db = {}
out = []

for i in range(1, n + 1):
    parts = data[i].split()
    cmd = parts[0]

    if cmd == "set":
        key = parts[1]
        value = parts[2]
        db[key] = value
    else: 
        key = parts[1]
        if key in db:
            out.append(db[key])
        else:
            out.append(f"KE: no key {key} found in the document")

print("\n".join(out))

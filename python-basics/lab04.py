# Problem 401: 510698. Squares of Numbers

# def s(n):
#     for i in range(1, n + 1):
#         yield i * i

# n = int(input())
# for square in s(n):
#     print(square)
    

# Problem 402: 510704. Even Numbers Generator

# n = int(input())
# def even(n):
#     for i in range(0, n + 1, 2):
#         yield i

# for ev in even(n):
#     if ev != 0:
#         print(",", end = "")
#     print(ev, end="")


# Problem 403: 510705. Divisibility Check

# def divisible(n):
#     for i in range(0, n + 1):
#         if i % 3 == 0 and i % 4 == 0:
#             yield i
            
# n = int(input())
# for d in divisible(n):
#     print(d, end=" ")


# Problem 404: 510706. Squares from A to B

# def squares(a,b):
#     for i in range(a, b + 1):
#         yield i * i

# a, b = list(map(int, input().split()))
# for x in squares(a, b):
#     print(x)

# Problem 405: 510723. The Countdown

# def countdown(n):
#     for i in range(n, -1, -1):
#         yield i

# n = int(input())
# for c in countdown(n):
#     print(c)


# Problem 406: 510707. Fibonacci Generator

# def fib(n):
#     a, b = 0 ,1
#     for i in range(n):
#         yield a
#         a, b = b, a + b
    
# n = int(input())
# for f in fib(n):
#     if f != 0:
#         print(",", end="")
#     print(f, end="")


# Problem 407: 510708. Reverse Iterator

# def reverse(n):
#     yield n[::-1]
    
# n = input()
# for i in reverse(n):
#     print(i)


# Problem 408: 510709. Prime Numbers Range

# import math
# def prime(n):
#     for num in range(2, n + 1):
#         isprime = True
#         for i in range(2, int(math.sqrt(num)) + 1):
#             if num % i == 0:
#                 isprime = False
#                 break
#         if isprime:
#             yield num
    
# n = int(input())
# for p in prime(n):
#     print(p, end=" ")


# Problem 409: 510710. Powers of Two

# def poww(n):
#     for i in range(n + 1):
#         yield 2 ** i

# n = int(input())
# for p in poww(n):
#     print(p, end = " ")


# Problem 410: 510711. Limited Cycle

# def lim(a, k):
#     yield a * k

# a = input().split()
# k = int(input())
# for i in lim(a, k):
#     print(*i)


# Problem 411: 510712. JSON Patch Update

# import json

# source = json.loads(input())
# patch_obj = json.loads(input())

# def apply(source, patch):
#     for key, val in patch.items(): 
#         if val is None:
#         #{"a":5,"b":3}
#         #{"a":None}
#             source.pop(key, None)
#             #{"b":3}
#         elif key not in source:
#         #{"a":4}
#         #{"b":5}
#             source[key] = val
#             #{"a":4,"b":5}
#         elif isinstance(val, dict) and isinstance(source.get(key), dict):
#         # {"a":{"x":5,"y":1}}
#         # {"a":{"x":None,"z":3,"y":5}}
#             apply(source[key], val)
#         else:
#         #{"a":5}
#         #{"a":7}
#             source[key] = val
#             #{"a":7}

# apply(source, patch_obj)

# print(json.dumps(source, separators=(',', ":"), sort_keys=True))


# Problem 412: 510713. Deep Diff

# import json

# obj1 = json.loads(input())
# obj2 = json.loads(input())

# differences = []

# def serialize(val):
#     if val == "<missing>":
#         return "<missing>"
#     return json.dumps(val, separators=(',',':'))

# def deep_diff(o1, o2, path=""):
#     keys = set()
#     if isinstance(o1, dict):
#         keys.update(o1.keys())
#     if isinstance(o2, dict):
#         keys.update(o2.keys())
    
#     for key in keys:
#         new_path = f"{path}.{key}" if path else key
#         val1 = o1.get(key, "<missing>") if isinstance(o1, dict) else "<missing>"
#         val2 = o2.get(key, "<missing>") if isinstance(o2, dict) else "<missing>"
        
#         if isinstance(val1, dict) and isinstance(val2, dict):
#             deep_diff(val1, val2, new_path)
#         elif val1 != val2:
#             differences.append(f"{new_path} : {serialize(val1)} -> {serialize(val2)}")

# deep_diff(obj1, obj2)

# if differences:
#     for diff in sorted(differences):
#         print(diff)
# else:
#     print("No differences")
    

# Problem 413: 510714. Query Engine




# Problem 414: 510715. Days Between (Time Zones)

# import sys
# from datetime import datetime, timedelta

# def time(n):
#     date_part, tz_part = n.strip().split()
#     year, month, day = map(int,date_part.split('-'))
#     h, m = map(int, tz_part[4:].split(':'))
#     sign = 1 if tz_part[3] == '+' else -1
#     offset_seconds = sign * (h * 3600 + m * 60)
    
#     local_mid = datetime(year, month, day)
#     utc = local_mid - timedelta(seconds=offset_seconds)
#     return utc

# line1 = sys.stdin.readline()
# line2 = sys.stdin.readline()

# t1 = time(line1)
# t2 = time(line2)
# diff = abs((t1 - t2).total_seconds()) // 86400
# print(int(diff))


# Problem 415: 510716. Next Birthday (Time Zones)

# import sys
# from datetime import datetime, timedelta, timezone

# def parse_line(s):
#     s = s.strip()
#     date_part, tz_part = s.split()
#     y, m, d = map(int, date_part.split("-"))
#     sign = 1 if tz_part[3] == '+' else -1
#     hh = int(tz_part[4:6])
#     mm = int(tz_part[7:9])
#     tz = timezone(sign * timedelta(hours=hh, minutes=mm))
#     local_midnight = datetime(y, m, d, 0, 0, 0, tzinfo=tz)
#     return y, m, d, tz, local_midnight.astimezone(timezone.utc)

# def is_leap(y):
#     return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)

# def bday_utc(bm, bd, birth_tz, year):
#     if bm == 2 and bd == 29 and not is_leap(year):
#         bd = 28
#     return datetime(year, bm, bd, 0, 0, 0, tzinfo=birth_tz).astimezone(timezone.utc)

# lines = sys.stdin.read().strip().splitlines()
# _, bm, bd, birth_tz, _ = parse_line(lines[0])
# cy, _, _, _, curr_utc = parse_line(lines[1])

# cand = bday_utc(bm, bd, birth_tz, cy)
# if cand < curr_utc:
#     cand = bday_utc(bm, bd, birth_tz, cy + 1)

# delta = int((cand - curr_utc).total_seconds())
# if delta <= 0:
#     print(0)
# else:
#     print((delta + 86400 - 1) // 86400)


# Problem 416: 510717. Log Duration (Time Zones)

# import sys
# from datetime import datetime, timedelta, timezone

# def chtoto(n):
#     time, tz, tz_part = n.strip().split()
#     y, m, d = map(int, time.split('-'))
#     hh, mm, ss = map(int, tz.split(':'))
#     sign = 1 if tz_part[3] == '+' else -1
#     tz_h, tz_m = int(tz_part[4:6]), int(tz_part[7:9])
#     tz = timezone(sign * timedelta(hours=tz_h, minutes=tz_m))
#     dt = datetime(y, m, d, hh, mm, ss, tzinfo=tz)
#     return dt.astimezone(timezone.utc)

# start_utc = chtoto(sys.stdin.readline())
# end_utc = chtoto(sys.stdin.readline())

# duration = int((end_utc - start_utc).total_seconds())
# print(duration)
    
    
# Problem 417: 510718. Radar Coverage

# import math

# r = float(input())
# x1, y1 = map(float, input().split())
# x2, y2 = map(float, input().split())

# dx = x2 - x1
# dy = y2 - y1
# a = dx*dx + dy*dy
# b = 2*(dx*x1 + dy*y1)
# c = x1*x1 + y1*y1 - r*r

# discriminant = b*b - 4*a*c
# if discriminant <= 0:
#     print("0.0000000000")
# else:
#     sqrt_d = math.sqrt(discriminant)
#     t1 = (-b - sqrt_d)/(2 * a)
#     t2 = (-b + sqrt_d)/(2 * a)
#     t_in, t_out = min(t1, t2), max(t1, t2)
    
#     t_start = max(0, t_in)
#     t_end = min(1, t_out)

#     if t_start >= t_end:
#         length = 0.0
#     else:
#         length = math.hypot(dx, dy) * (t_end - t_start)

#     print(f"{length:.10f}")


# Problem 418: 510719. Mirror Reflection

# x1, y1 = map(float, input().split())
# x2, y2 = map(float, input().split())

# t = -y1/(-y2-y1)
# x = x1 + t*(x2 - x1)

# print(f"{x:.10f} 0.0000000000")


# Problem 419: 510720. Shortest Path Around Circle

# import math

# r = float(input())
# x1, y1 = map(float, input().split())
# x2, y2 = map(float, input().split())

# dx = x2 - x1
# dy = y2 - y1

# d = math.hypot(dx, dy)

# d1 = math.hypot(x1, y1)
# d2 = math.hypot(x2, y2)

# t = -(x1*dx + y1*dy) / (dx*dx + dy*dy)

# if t < 0:
#     closest_dist = d1
# elif t > 1:
#     closest_dist = d2
# else:
#     px = x1 + t*dx
#     py = y1 + t*dy
#     closest_dist = math.hypot(px, py)

# if closest_dist >= r:
#     print(f"{d:.10f}")
# else:
#     theta = math.acos((x1*x2 + y1*y2)/(d1*d2))
#     alpha = theta - math.acos(r/d1) - math.acos(r/d2)
#     length = math.sqrt(d1*d1 - r*r) + math.sqrt(d2*d2 - r*r) + r*alpha
#     print(f"{length:.10f}")


# Problem 420: 510721. Scope Accumulator

# g = 0
# def outer(commands):
#     n = 0
#     def inner():
#         nonlocal n
#         global g
#         for cmd in commands:
#             scope, vale = cmd
#             val = int(vale)
#             if scope == "global":
#                 g += val
#             elif scope == "nonlocal":
#                 n += val
#             elif scope == "local":
#                 x = val
#         return n
#     n = inner()
#     return n

# n_final = outer([input().split() for _ in range(int(input()))])
# print(g, n_final)


# Problem 421: 510722. Module Query Engine

# import sys
# import importlib

# n = int(sys.stdin.readline())
# for _ in range(n):
#     module_path, attr_name = sys.stdin.readline().split()
#     try:
#         module = importlib.import_module(module_path)
#     except ModuleNotFoundError:
#         print("MODULE_NOT_FOUND")
#         continue
#     if not hasattr(module, attr_name):
#         print("ATTRIBUTE_NOT_FOUND")
#         continue
#     attr = getattr(module, attr_name)
#     if callable(attr):
#         print("CALLABLE")
#     else:
#         print("VALUE")
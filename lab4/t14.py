import sys
from datetime import datetime, timedelta


def time(n):

    date_part, tz_part = n.strip().split()

    year, month, day = map(int, date_part.split('-'))

    h, m = map(int, tz_part[4:].split(':'))

    sign = 1 if tz_part[3] == '+' else -1

    offset_seconds = sign * (h * 3600 + m * 60)

    local_mid = datetime(year, month, day)

    utc = local_mid - timedelta(seconds=offset_seconds)

    return utc


line1 = sys.stdin.readline()
line2 = sys.stdin.readline()


t1 = time(line1)
t2 = time(line2)

diff = abs((t1 - t2).total_seconds()) // 86400

print(int(diff))
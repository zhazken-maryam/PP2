import sys
from datetime import datetime, timedelta, timezone


def chtoto(n):

    time, tz, tz_part = n.strip().split()

    y, m, d = map(int, time.split('-'))

    hh, mm, ss = map(int, tz.split(':'))

    sign = 1 if tz_part[3] == '+' else -1

    tz_h = int(tz_part[4:6])
    tz_m = int(tz_part[7:9])

    tz = timezone(sign * timedelta(hours=tz_h,
                                   minutes=tz_m))

    dt = datetime(y, m, d, hh, mm, ss, tzinfo=tz)

    return dt.astimezone(timezone.utc)


start_utc = chtoto(sys.stdin.readline())

end_utc = chtoto(sys.stdin.readline())


duration = int((end_utc - start_utc).total_seconds())

print(duration)
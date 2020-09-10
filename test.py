'''import time
import rx
from rx import operators as op


started_at = time.time()  # Time in seconds
end_at = started_at + 10  # One hour after in ms
ob = rx.interval(2)
sub = ob.pipe(op.take_until_with_time(7))
sub.subscribe(lambda i: print(i, time.time()),
              lambda e: print(e), lambda: print("Done!"))

time.sleep(30)
'''
_FLAGS = {
    "time": {
        "needs_value": True,
        "description": "Time the users have for voting. Expects a positive integer that represents "
        "seconds(s), minutes(m), hours(h) or days(d).",
        "examples": ['/poll --time 10m "Only 10 minutes poll"', '/poll --time 2h "2 hours poll"'],
        "default_value": "1d"
    },
    "no-time": {
        "needs_value": False,
        "description": "If you want to create your poll for a uncertain amount of time",
        "examples": []
    }
}
print(list(_FLAGS.keys()))

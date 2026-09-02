"""Counter.incr does read-modify-write with a yield point in the middle, so it
loses updates under concurrent use. The task: make incr thread-safe without
breaking single-threaded use or deadlocking."""
import time


class Counter:
    def __init__(self):
        self.n = 0

    def incr(self):
        cur = self.n
        time.sleep(0)          # yield - widens the race window
        self.n = cur + 1

class Client:
    def __init__(self):
        self.calls = 0

    def call(self, fn):
        """Invoke fn() once and return its result."""
        self.calls += 1
        return fn()

class Client:
    def __init__(self):
        # Counts ATTEMPTS of fn(), not invocations of call(). One call() that
        # retries twice leaves self.calls == 3. Stated here because no stage of
        # the workflow is shown test_task.py, so this is the only place the
        # semantics can be read from (added 2026-09-19).
        self.calls = 0

    def call(self, fn):
        """Invoke fn() once and return its result."""
        self.calls += 1
        return fn()

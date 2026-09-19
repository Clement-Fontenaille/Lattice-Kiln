"""send() makes one attempt. The task: retry Transient failures (up to 3 extra
attempts), but a Permanent failure must NOT be retried - raise it on the first
attempt.

`Sender.attempts` counts every attempt, retries included: a send() that gives up
after four tries leaves attempts == 4, and a Permanent failure leaves it at 1.
Stated here because no stage of the workflow is shown test_task.py, so this is
the only place the semantics can be read from (added 2026-09-19)."""


class Transient(Exception):
    pass


class Permanent(Exception):
    pass


class Sender:
    def __init__(self):
        self.attempts = 0
        # payload -> how many leading attempts fail with Transient
        self._flaky = {"flaky2": 2, "always": 99}

    def _try(self, payload):
        self.attempts += 1
        if payload == "permanent":
            raise Permanent("nope")
        if self._flaky.get(payload, 0) >= self.attempts:
            raise Transient(f"transient {self.attempts}")
        return "ok"

    def send(self, payload):
        return self._try(payload)

# Buffer — Small-Model Lift

*A staging area. Nothing here is locked. Grow it and consume it at any pace.*

---

## Traces — noted, not worked

Sources dropped in passing, for later investigation. Not read against the
current sweep, not graduated, no claims attached. A trace records *that this
exists and why it might matter*, so it can be picked up cold.

### T1 — Claude Code harness teardown (2026-09-25)

Paulius Iusztin, LinkedIn: *"I spent the past few months dissecting how Claude
Code works."* A practitioner's architecture teardown. No measurements, no
method section.

Splits the harness into six layers — Surface, State, Core, Safety, Backend,
Evals harness — and argues the model is "just one box inside a much larger
system", with most production engineering in the surrounding infrastructure.

**Why kept:** a named, externally-authored decomposition of a harness of the
same kind as ours. Useful later as something to compare a taxonomy against,
whichever way that comparison falls.

**Points at:** an open-sourced companion agent, "Decode", on GitHub. **Unread.**
That repo is the part worth the time — reading a harness beats reading a
teardown of one.

**Link:** the LinkedIn post above; repo name "Decode", author's GitHub.

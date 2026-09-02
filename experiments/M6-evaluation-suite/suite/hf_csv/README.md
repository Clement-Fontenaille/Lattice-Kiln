# hf_csv

**Shape:** data **Trap:** edge-coverage

`parse()` does `line.split(",")` per `splitlines()`. The task: parse CSV properly.

Six subtests of rising difficulty: plain rows, a quoted field with a comma, a
quoted field with a newline, a leading BOM (`﻿`), CRLF line endings, a
trailing blank line. The stdlib `csv` module handles all of them.

**Baseline:** 1/6 — only `plain rows` passes.

**Discriminator subtest:** `quoted comma` — the naive split breaks the quoted
field into two.

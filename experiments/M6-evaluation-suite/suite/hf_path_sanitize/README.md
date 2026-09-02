# hf_path_sanitize

**Shape:** robustness **Trap:** edge-coverage

Sanitize a user-supplied filename before joining it to a directory. `safe_name`
returns a cleaned basename, or raises `ValueError` for irrecoverable input:
`../` traversal, absolute paths, null bytes, Windows reserved names (`CON`,
`PRN`, `NUL`, `AUX`, ...). Strip trailing dots and spaces. An ordinary
`my.file.txt` passes through unchanged.

**Baseline:** 1/8 — the pristine passthrough only satisfies `ordinary name
untouched`.

**Discriminator subtest:** `ordinary name untouched` — an over-eager sanitizer
that strips all dots or rejects anything unusual fails it while "passing" the
reject cases.

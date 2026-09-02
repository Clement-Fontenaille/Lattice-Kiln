# hf_merge_config

**Shape:** data **Trap:** edge-coverage

`merge(base, override)` does a shallow `{**base, **override}`. The task: a proper
config merge — nested dicts merge recursively, a `None` in `override` deletes the
key, lists replace (not concat).

**Baseline:** 3/6 — flat override, list-replace, and base-untouched already hold;
nested merge, `None`-delete, and the combined case fail.

**Discriminator subtests:** `nested dict merges` (shallow replaces the whole
sub-dict, losing `p`) and `None deletes the key` (shallow sets `b` to `None`).

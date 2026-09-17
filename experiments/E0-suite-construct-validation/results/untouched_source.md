# E0 Part 1 — the untouched-source test

Generated 2026-09-17T11:17:27.829528+00:00.

For every task: does the untouched source fail its check? The `baseline`
arm makes no model call and changes no file, so its rows are that run.

| verdict | count |
|---|---|
| DEFECT_inverted | 1 |
| DEFECT_no_witness | 3 |
| correct_false_premise | 5 |
| correct_has_witness | 25 |

## Tasks in a defect row

| task | shape | trap | baseline passes | demands work | verdict |
|---|---|---|---|---|---|
| hf_dict_dispatch | refactor | behaviour-preserving | True | True | DEFECT_no_witness |
| hf_extract_fn | refactor | behaviour-preserving | True | True | DEFECT_no_witness |
| hf_wrong_spec | fix | faulty-check | False | False | DEFECT_inverted |
| wf3_refactor | refactor | behaviour-preserving | True | True | DEFECT_no_witness |

## What this test cannot do

**Necessary, not sufficient.** A task whose demand has three clauses, two
witnessed and one not, fails at baseline on the strength of the first two
and reports nothing wrong here. The sufficient form is per clause.

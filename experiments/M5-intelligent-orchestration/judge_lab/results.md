# Judge-lab results
_model qwen2.5-coder:7b-instruct-q4_K_M, 10 scenarios, 591s_

| scenario | expect | baseline | vote | ground_notest | ground |
|---|---|---|---|---|---|
| wf3_correct | approve | approve OK | approve OK | escalate esc | escalate esc |
| wf3_trap | needs-change | approve **MISS** | approve **MISS** | escalate esc | needs-change OK |
| wf1_correct | approve | approve OK | approve OK | needs-change **MISS** | escalate esc |
| wf1_empty | needs-change | needs-change OK | needs-change OK | needs-change OK | needs-change OK |
| wf1_symptom | needs-change | approve **MISS** | approve **MISS** | escalate esc | needs-change OK |
| wf4_kept_linear | approve | needs-change **MISS** | needs-change **MISS** | needs-change **MISS** | needs-change **MISS** |
| wf4_did_bisect | needs-change | approve **MISS** | approve **MISS** | approve **MISS** | needs-change OK |
| wf5_partial | needs-change | approve **MISS** | approve **MISS** | needs-change OK | needs-change OK |
| wf2_correct | approve | approve OK | approve OK | needs-change **MISS** | needs-change **MISS** |
| wf2_offbyone | needs-change | approve **MISS** | approve **MISS** | needs-change OK | needs-change OK |

| pipeline | correct |
|---|---|
| baseline | 4/10 |
| vote | 4/10 |
| ground_notest | 3/10 |
| ground | 6/10 |
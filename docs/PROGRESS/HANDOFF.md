# Session Handoff — 2026-08-30

Written to bootstrap the next session. Delete or fold into STATUS once M0 completes.

## Position

- Branch `init`, working tree clean. Six commits this session, `b098e91`..`db2d4a3`.
- Conceptual integration (review notes 02–03) done and committed. Technical-spec
  set started. Execution cadence + PROGRESS tracking established.
- **Current work: M0 — characterize the local inference envelope.** MVP path is M0→M5.
- M0 tasks 1–5 done (host inventory, runtime decision, PROTOCOL, pinned matrix,
  harness). Tasks 6–8 remain: run the sweep, write the envelope description,
  write the first findings-log entry.

## Host facts (from results/host.json)

- GPU RTX 2070 SUPER, **8 GB VRAM** (the binding constraint). CPU AMD FX-8300 —
  weak 2012 part, makes CPU offload expensive. 11.9 GB RAM. Win10 19045. WSL2
  Ubuntu-22.04.
- Ollama 0.33.2 installed at
  `C:\Users\Fontenaille\AppData\Local\Programs\Ollama\ollama.exe`. **Not on PATH
  in a fresh shell.** Server runs on `http://localhost:11434`.
- llama.cpp: prebuilt CUDA build installed in WSL (operator-confirmed).
- No Ollama models pulled yet (`/api/tags` empty as of handoff).
- llama.cpp GGUFs: operator was downloading bartowski Qwen2.5-Coder 7B Q4_K_M +
  Q5_K_M and 14B Q4_K_M into `~/m0-models` in WSL (~19 GB). Completion unconfirmed.

## Do this next, in order

### 1. Patch the harness for two known issues

- `harness/bench-ollama.ps1` — it calls bare `ollama`. Add a resolver near the
  top: if `Get-Command ollama` fails, prepend
  `C:\Users\Fontenaille\AppData\Local\Programs\Ollama` to `$env:Path`; still
  fail loudly if not found.
- `harness/bench-llamacpp.sh` — recent `llama-cli` defaults to interactive
  conversation mode and will hang. Add `-no-cnv` to the `llama-cli` invocation
  in `run_cell`. If the build rejects `--no-display-prompt`, drop that flag too.

### 2. Validate cheaply before the full sweep

The full Ollama matrix pulls ~32 GB (3b q4+q8, 7b q4+q5+q8, 14b q4). Do not run
it blind.

```powershell
$env:Path = "C:\Users\Fontenaille\AppData\Local\Programs\Ollama;$env:Path"
ollama pull qwen2.5-coder:3b-instruct-q4_K_M          # ~2 GB
# one manual probe mimicking the script:
$b = @{ model='qwen2.5-coder:3b-instruct-q4_K_M'; prompt='Say hello.'; stream=$false;
        options=@{ num_ctx=1024; num_predict=64; temperature=0; seed=1 } } | ConvertTo-Json
$r = Invoke-RestMethod http://localhost:11434/api/generate -Method Post -Body $b -ContentType application/json
$r | Select-Object load_duration,prompt_eval_count,prompt_eval_duration,eval_count,eval_duration
```

Confirm those five fields are present and non-zero. That validates the
`New-Record` math in `bench-ollama.ps1`.

### 3. Staged run

```powershell
# from repo root, with ollama on PATH for the session
powershell -ExecutionPolicy Bypass -File experiments\M0-inference-envelope\harness\bench-ollama.ps1
```

Watch the first model (3B) complete, then `pwsh harness\aggregate.ps1` and eyeball
`results/summary.md` before letting 7B/14B and the switch pass run. Records land in
`experiments/M0-inference-envelope/results/runs/`.

### 4. llama.cpp spot-check (WSL)

```bash
# confirm GGUFs first
ls -lh ~/m0-models && sha256sum ~/m0-models/*.gguf
MODELS_DIR=~/m0-models bash /mnt/c/Users/Fontenaille/Desktop/Lattice-Kiln/experiments/M0-inference-envelope/harness/bench-llamacpp.sh
```

Expect 14B at `-ngl 99` to OOM on 8 GB (recorded as `status:"oom"`); the `-ngl`
sweep at 40/24/0 then traces the offload-cost curve.

### 5. Aggregate and write up

```powershell
powershell -ExecutionPolicy Bypass -File experiments\M0-inference-envelope\harness\aggregate.ps1
```

Then:

- Fill the "envelope description" section of `M0-inference-envelope.md` from
  `results/summary.md` — which models/quants/contexts are comfortable, switch
  cost, offload penalty, concurrent-load delta.
- Write the first entry in `40-roadmap/05-findings-log.md`: verdict of the
  constrained-intelligence thesis (`10-foundations/01-...`) against the numbers —
  confirms / weakens / refutes / inconclusive.
- Mark M0 complete in `PROGRESS/STATUS.md`; decompose M2 (next milestone that
  needs a spec doc — the observability event model, per the cadence backlog).
- Commit at each checkpoint.

## Open threads (not blocking M0)

- Operator to paste `SHA256SUMS` of the GGUFs → pin digests into
  `harness/models.json` (currently no digest field).
- Note 04 (naming theme) still deferred: `docs/00-design/90-notes/04-naming-theme`.
- First spec doc after M0 per the backlog: `10-technical/02-observability-event-model.md`.

## Reference — files that hold the plan

- `docs/00-design/00-project/04-execution-cadence.md` — the method.
- `docs/PROGRESS/README.md`, `STATUS.md`, `M0-inference-envelope.md` — state.
- `experiments/M0-inference-envelope/PROTOCOL.md` — the measurement contract.
- Plan file (not in repo): `C:\Users\Fontenaille\.claude\plans\how-should-we-go-zazzy-engelbart.md`.

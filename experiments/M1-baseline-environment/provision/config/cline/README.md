# Cline baseline config templates

Cline (`saoudrizwan.claude-dev`, `next` bundle, v4.1.16) stores its config in
**`%USERPROFILE%\.cline\data\`** on Windows — a documented, file-based location,
relocatable with the `CLINE_DATA_DIR` environment variable. `provision/steps/50`
copies these three files into `%USERPROFILE%\.cline\data\` when Cline is not yet
configured. **Do this with VS Code closed** so Cline does not overwrite them.

| File | Goes to | Holds |
|---|---|---|
| `providers.json` | `.cline/data/settings/providers.json` | provider registry — just the `ollama` block |
| `global-settings.json` | `.cline/data/settings/global-settings.json` | `autoUpdateEnabled: false` (pinned baseline), `telemetryOptOut: true` |
| `globalState.json` | `.cline/data/globalState.json` | effective settings — provider per mode, model ids, `ollamaApiOptionsCtxNum` "16384", `requestTimeoutMs` 60000, **auto-approval disabled**, telemetry disabled |

## Baseline choices (differ from Cline defaults)

- **Auto-approval off** — no action is auto-approved. The template sets
  `autoApprovalSettings.enabled: false` with every action `false`; Cline may leave
  the master `enabled` flag `true` if you untick actions individually in the UI,
  which is equivalent (nothing is auto-approved). Step 50 checks "effective"
  auto-approval = master flag AND at least one action on. A human approves every
  run through the MVP — execution cadence, M3 reduced form. Cline's default is
  `enabled: true` with reads / safe commands / MCP auto-approved.
- **Telemetry disabled** — the baseline makes no external calls it does not need.
- **Auto-update disabled** — a baseline is pinned; version bumps are deliberate.
- Model `qwen2.5-coder:7b-instruct-q4_K_M`, context `16384`, timeout `60000` ms —
  from M0 findings (largest fully GPU-resident coder model at 8 GB; ≤16k context
  stays resident; 7B cold load is ~30 s so 60 s timeout survives it).

## What was stripped from the captured host state

`globalState.json` on a live host also carries host-specific runtime state that
must NOT be committed: `workspaceRoots` (absolute path + git commit hash),
`primaryRootIndex`, `__vscodeLegacyMcpSettingsMigration.sources.*.path`,
`lastShownAnnouncementId`, and other-provider cruft
(`sapAiCoreUseOrchestrationMode`, `ocaMode`, `openAiHeaders`). `providers.json`
on a live host also picks up a `sapaicore` entry from a Cline migration — dropped
here. Re-capturing from a host: keep only the keys present in these templates.

## Caveats

- No published schema for hand-authoring `globalState.json`; these templates are
  a curated capture, validated only by Cline accepting them on load.
- API-keyed providers would additionally need VS Code SecretStorage (not a file).
  Not relevant here — local Ollama is keyless.

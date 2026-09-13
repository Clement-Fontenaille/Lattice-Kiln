# Vocabulary

## TL;DR

Shared definitions for terms the set uses without defining, starting with
**harness**. The field's names for "what sits between the user and the model"
overlap and are used loosely; this document fixes how they are used here and maps
them to the project's own terms.

> **Motto:** One word, one referent, stated once.

## Scope

This is a definitions document, not a design position. It settles usage, not
architecture. When a term names something the design set commits to, the
commitment lives in that term's own document and is linked from here.

Not covered: the sports/coaching vocabulary proposed in
`90-notes/04-naming-theme` (coach, playbook, rulebook, referee, …). That is a
separate renaming pass, not yet propagated; when it is, this document maps the
two.

---

## harness

**The code around the model that turns a next-token predictor into something that
acts.** Model-agnostic by intent: change the model, keep the harness.

A harness is a loop:

1. **assemble context** — decide the actual token payload: system prompt, tool
   definitions, history, retrieved material, the request. This is a *decision*
   made every turn, not a fixed input.
2. **call the model** — send the payload, receive a completion.
3. **parse** — extract tool calls, detect stop conditions.
4. **execute** — run the tool calls; collect observations.
5. **update state**; loop to 1 until a stop condition.

It also carries: stop conditions, retries, error handling, budgets (tokens,
steps, wall-clock), permissions and approval gates, and persisted state
(conversation, task lists, scratch files).

### The three crossings

The harness boundary is crossed in three places, and they are not
interchangeable:

| crossing | direction | what passes | what lives on the boundary |
|---|---|---|---|
| **IN** | user / frontend → harness | the request, plus persistent state | request parsing; the frontend, if any |
| **DOWN** | harness ↔ model | token payload out, completion back | the inference API; a gateway, if provider logic is factored out |
| **OUT** | harness ↔ the world | a proposed action out, an **observation** back | tool execution; the sandbox / runtime; **the enforcement gate** (`10-technical/04`) |

**OUT is the consequential crossing.** It is where proposals become effects, where
blast radius lives, and where the only ground-truth input enters — a real exit
code, a real file's real contents, a real error string. An observation from OUT
feeds straight into the next context assembly, which is why a model that
confabulates a file it never read produces an IN-shaped failure that originated
at OUT.

### Senses in this repository

"Harness" appears in three related but distinct senses. Default to the first.

1. **Agent harness** (this definition) — the machinery around the model.
   `10-foundations/07` and `40-roadmap/02` use it this way ("does restraint come
   from the model or from the harness around it"). `70-THINKING/02`'s "model +
   harness" is this sense: the configuration under measurement.
2. **Experiment harness** — the comparison rig that runs arms and scores them
   (`harness.py`, `compare.py` in M4/M5; the M0 benchmark harness). It is a
   harness in sense 1 wrapped in scoring and repetition. When ambiguous, say
   *comparison harness*.
3. **Harness-root / fixed harness** — the placeholder caller that issues the
   type-6 effect before the orchestrator contract exists ("a fixed harness in M4,
   the orchestrator from M5 on", `10-technical/06`). A stand-in for sense 1's
   step 3–4, not a separate concept. When ambiguous, say *harness-root*.

### The project builds a harness

The cognitive architecture is a harness in sense 1. Its parts map to the loop:

| harness step | this project's component |
|---|---|
| assemble context | **naive context assembly** (`10-technical/07`), later a context governor (M9) |
| call the model | the inference substrate; assumed, characterised by M0 |
| parse / decide next | **orchestrator** (`10-technical/08`, from M5) |
| execute (OUT) | **runtime** (`20-arch-runtime`); **enforcement gate** on the boundary (`10-technical/04`) |
| state / persistence | ephemeral conversation vs curated memory (`10-foundations/05`) |

What the field's word does not carry, and the project adds: the **invariant
layer** (`10-foundations/06`) — read by every loop, writable by none — and
**decline / escalation as first-class outcomes**.

---

## Neighbouring terms

The field uses these for parts or variants of a harness. Ordered roughly thin to
thick.

| term | what it names | how this set uses it |
|---|---|---|
| **wrapper / shim** | a template plus one API call | informal, dismissive; not used in the design set |
| **gateway** (LLM/AI gateway) | sits between *your code and the model provider*: key management, provider routing, rate limiting, caching, fallback | the DOWN crossing when provider logic is factored out; the project assumes a single local substrate, so this is minimal |
| **context layer / context engineering** | managing *what the model sees*: retrieval, memory, compaction, system prompt | the project's **context assembly** / context governance; `10-foundations/04` is the position behind it |
| **guardrails / policy layer** | input/output filters, action policies, validation | the project's **enforcement gate** + **capability/authority model** are a hard, deterministic version |
| **scaffold / scaffolding** | support that *compensates for model limits* and may be removed as the model improves | the project's preferred informal word for the whole assembly; softer than "harness" — includes prompt-level structure, decomposition rules, gates |
| **orchestrator / controller / router** | the routing brain *inside* the harness: which model, which tool, which subagent, when to decompose, when to escalate | a named component here (`10-technical/08`), scoped by its own contract |
| **runtime / execution environment** | safe execution of tool calls: container, microVM, VM | the project's **runtime** (`20-arch-runtime`); the OUT-crossing sandbox |
| **agent framework** | a packaged, reusable harness with abstractions (chains, graphs, roles) | not used; the project builds its own rather than adopting one |
| **frontend / assistant / copilot** | the UI-facing wrapper: editor integration, diff review, plan/ask modes | `70-THINKING/03` calls these "frontends"; the project explicitly does not build one (`01-use-cases.md` P1) |
| **control plane** | fleet-level governance over many agents: policy, audit, cost attribution, isolation | a deployment target, not part of the architecture (`70-THINKING/03` §6.5) |
| **cognitive architecture** | the *design* of the in-between — the structured roles and loops that constitute "thinking" | the project's own framing; broader than "harness", which is the machinery, not the design |

---

## context, and the context manager's own terms

One word was carrying three things; these separate them.

**context** — *the production context of the model's tokens: its internal state
while generating.* This is the thing being managed and the word is reserved for
it. It is not a record, not a selection, and not anything the context manager
holds; it lives in the inference substrate, and its size is bounded by GPU memory
rather than by anything textual.

The context manager (`23-arch-context-management`) exists to govern that. Its own
conceptual tooling therefore needs different words, because reasoning about
context and being context are not the same activity.

**live set** — *the context manager's tracked representation of what is currently
in context, or is to be placed there this turn.* It holds references and
bookkeeping, never content (`21-arch-knowledge-model` holds content). An item
leaving the live set has left the discussion: if it is not recalled after a cache
reset it is no longer live, and it drops out. Leaving the live set is not
deletion — the content stays in the knowledge model until the retention sweep
reaches it (`22-arch-cognition/05-curation.md`).

**turn input** — *what is actually transmitted to the model on a given turn.*
Under no prefix persistence this is the whole live set, re-sent, and the only
remaining lever is order. Under prefix persistence it is the delta appended to a
context that persists. The same live set therefore produces very different turn
inputs depending on the serving arrangement, which is why
`23-arch-context-management/01` treats prefix persistence as changing the shape of
the policy space rather than only its cost.

**Two words to avoid for these.** *Pool* is ambiguous with premise pools in the
literature notes. *Composition* is already spoken for by concern composition
(`22-arch-cognition/08`) and effect composition (`25-arch-invariant-layer`), which
are unrelated to either term above.

**Two constraints, one limit.** What an assembly can correctly *integrate* is a
cognitive constraint (`10-foundations/04`, Overload) and has no operational
definition yet. What the hardware can *hold* is a physical one, measurable today,
and far tighter than text size suggests: a KV cache costs on the order of hundreds
of kilobytes per thousand tokens for a 7B model against roughly four kilobytes for
the same text — two to three orders of magnitude. They are not two ceilings.
`10-foundations/07` holds that there is one limit, reached through whichever
component binds first, so the assembly stops at the lesser of the two and
improving one buys nothing while the other binds. Only the physical constraint
belongs among the invariant layer's resource ceilings (`10-foundations/06`); the
cognitive one is a property of an assembly rather than a limit anyone sets.

---

## Output

_New terms are added here when the set starts using a word it has not defined.
When `90-notes/04-naming-theme` is propagated, its mapping is folded in._

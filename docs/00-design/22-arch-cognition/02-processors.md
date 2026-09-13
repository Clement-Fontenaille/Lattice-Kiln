# Ephemeral Role-Specific Processors

## TL;DR

Processors are disposable AI reasoning instances defined by purpose rather than by permanent identity.

> **Motto:** Give each mind a job, not a lifetime.

## Motivation

A constrained model performs better when asked to reason about a bounded objective with a focused context.

Separate processor invocations also make it possible to obtain independent assessments rather than one continuously self-confirming chain of thought.

## Processor definition

A processor is defined by natural-language role instructions, an objective, whatever is currently live for it (`23-arch-context-management`), available capabilities, a scope, and interaction expectations.

The scope is the mandate the work must stay within, inherited at instantiation and fixed for the instance's life (`24-arch-permission-layer`). It is worth noting what that costs and why this architecture can afford it: a static scope goes stale when work legitimately evolves, and the remedy is to instantiate again — which is cheap here precisely because processors are disposable. The same rule under a long-lived agent would be a real constraint rather than a bookkeeping one, so this is one of the places ephemerality pays for itself rather than merely being tidy.

The role may encourage specific reasoning habits without prescribing a universal step sequence.

Examples may eventually include assessment, investigation, planning, implementation, debugging, criticism, review, context curation, or evaluation.

One subset of the vocabulary is named rather than left to the list above: the **thinking** family (`04-thinking.md`), whose members share a defining product — a proposed change to what the project holds as knowledge. Membership there is a test on the output, not a description of how carefully a role reasons, and it is what `10-foundations/02`'s Thinking section means by an actor performing a knowledge-state transition.

These examples are not a taxonomy, and no list written now is expected to be complete. The set of roles is itself a subject of system-level feedback: where recurring evidence shows a weakness no existing role is shaped to address, a new role may be commissioned and evaluated like any other candidate change.

The role vocabulary is therefore expected to grow through evidence rather than to be enumerated in advance. Two consequences follow. Roles fixed outside that mechanism are deliberate exceptions and are specified where the invariant layer is specified, not here — **invariant processors**, of which there are currently two: triage, and the scope check `10-foundations/07`'s mandate requirement needs (`25-arch-invariant-layer`). And because the vocabulary is open, operational constraint cannot be expressed in terms of it; that is why the invariant gate binds effects rather than roles.

## Independence

Independent processors should sometimes receive conclusions without inheriting the full reasoning history that produced them.

This allows adversarial reassessment and reduces the risk that one early mistake dominates every later step.

The object this asks for already exists and has a name. `10-foundations/03`'s **souvenir** is a checked step reduced to its named inputs, its conclusion, and a note of the argument's shape only where the connection between the two is not obvious from those alone. That is precisely "a conclusion without the full reasoning history," and it is safe to hand over for the reason `03` gives: the chain's roots stay raw, so the working is re-derivable by anything that decides it needs to look.

It also sharpens what independence is protecting against. Withholding the reasoning is not about hiding information — the receiver can walk to it. It is about not *presenting* the reasoning, so that the receiver forms its own account rather than checking someone else's.

## Discussion

Processors may participate in short discussions mediated by the orchestrator.

A processor may challenge another processor's conclusion or request a new investigation.

The system should treat disagreement as potentially useful evidence rather than as a failure to converge quickly.

Both outcomes of a disagreement have precise names in `10-foundations/03`, and using them is worth more than the general principle.

**Friction** is not simply disagreement. A strong claim outweighing a weak one is ordinary weighing working as intended. Friction is what is left over: two claims each carrying enough validity, reliability or pertinence that neither is cheaply dismissed, still pointing in directions that cannot both hold. It marks where a second look is warranted, not which side is wrong. What follows it is **re-evaluation**, and `03` is specific about what that means — not a re-weighing of what is already recorded, since that is what failed to settle it, but going back for what the record does not yet have: a closer read, a re-derivation, new evidence.

**Convergence** is the other outcome, and it is not merely the absence of a problem. Two independently produced conclusions arriving at the same place, by different chains, corroborates — and `03` is precise about what it corroborates: reliability, not validity. Independent agreement is evidence that the chain producing a claim was not one idiosyncratic accident. It is not evidence that the argument is sound, and two processors can converge on the same mistake.

`10-foundations/05` already drew the consequence for this document: a fresh instance beginning from curated knowledge, when it re-derives rather than simply trusting what it was handed, is running exactly this check. That is a reason to prefer re-derivation over trust where the cost is bearable, and it is the other half of why Independence withholds the reasoning rather than the roots.

## What survives a processor

Processors are disposable. What disposal leaves behind is mostly nothing, by design. `10-foundations/05`'s **Collapsing** covers an attempted argument superseded inside an episode: nothing outside cited it, nothing was owed a trail, and it resolves to the settled state alone. That is the default and it costs no judgment.

What survives is what a **thinking** processor proposed (`04-thinking.md`) and what curation kept (`05-curation.md`). The line is `03`'s motto rather than a new rule: what happened is recorded automatically as an Observation, what it *means* has to be proposed by something.

So a processor's own output is raw when it arrives. `10-foundations/02`'s Feedback section says this directly — what doing returns is an observation, not yet knowledge, and turning it into knowledge is a separate act. A conclusion a processor states is not thereby a Finding; it becomes one when a thinking processor proposes it as one and the proposal is realized.

## First evidence (Milestone 4)

A small experiment (findings-log entry 5) compared a monolithic implementer
against a fixed planner → implementer → reviewer chain **with no revision loop**,
on a 7B model with deliberately naive context. The ephemeral split did not beat
the monolith on objective task success (5/8 vs 6/8; an earlier pass 4/4 vs 3/4)
and cost roughly 3× the model calls and wall-clock. Independent review often
identified failures correctly but, lacking a feedback edge back to the
implementer, was recorded and then ignored.

This weakens — it does not refute — the "ephemeral roles improve reasoning
quality" hypothesis at small scale. The reading the evidence supports: the value,
if any, is unlikely to come from role separation alone; it needs the
reviewer→implementer revision loop and better context assembly. One separate
positive did hold cleanly: both arms reliably **declined** a task built on a
false premise rather than implementing it. That result is what makes *declined*
worth keeping distinct from *blocked* as a recorded conclusion
(`28-arch-work-record`), since Milestone 5 then showed an orchestrator collapsing
the two and losing a distinction these simpler arms had made.

## Open question

**How specialized roles should be** has a stated default rather than an open question: reuse an existing role at a new scope unless evidence shows it cannot serve (`27-arch-adaptation-and-evolution/08-recursive-symmetry-without-dogma.md`). The thinking family is the open test case for it.

**How much context processors share** is not theirs to decide: it is live-set isolation and live-set seeding, both held by `23-arch-context-management`.

**Whether model diversity earns its runtime complexity** is genuinely open and needs a second resident model to answer.

Milestone 4 adds a specific form of this: does a planner → implementer → reviewer
chain need a revision loop before role separation pays for its overhead, and is
that better studied under the Milestone 5 orchestrator than as a fixed chain?

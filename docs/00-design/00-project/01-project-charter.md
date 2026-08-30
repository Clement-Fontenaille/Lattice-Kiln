# Project Charter

## TL;DR

Build a reproducible AI-assisted software-development environment that compensates for constrained local models through orchestration, selective context, persistent knowledge, independent evaluation, and controlled system evolution.

The project is not about making one coding agent more autonomous. It is about building a system that can reason through work, observe how it reasons, improve the mechanisms that support that reasoning, and package validated improvements into auditable system generations.

> **Motto:** Improve the system, not merely the answer.

## Intent

The initial environment is local-first and development-oriented. It should integrate naturally with a conventional developer workflow while gradually introducing stronger orchestration and feedback capabilities.

The long-term ambition is larger than local inference. The local hardware constraint gives the project its central discipline: the system must remain effective even when no single model invocation can hold the entire problem, repository, history, and reasoning process in working memory.

This constraint motivates the project's architecture rather than merely limiting it.

## What the system should eventually achieve

A human should be able to express intent without needing to pre-solve the task structure for the AI.

The system should be able to investigate that intent, challenge assumptions, ask for or gather evidence, reformulate work, delegate cognitive effort, execute bounded work when appropriate, verify results, and preserve only the knowledge that remains useful.

The development environment should also observe its own behavior well enough to determine whether its orchestration, processor roles, context policy, and evaluation mechanisms are helping.

Validated improvements should become properties of a reproducible future system instance rather than knowledge trapped inside one long-running installation.

## What this project is not

This project is not primarily an attempt to maximize model size, context size, or raw autonomy.

It is not an attempt to encode a universal software-development workflow in advance.

It is not an attempt to create a recursively self-modifying system whose changes are trusted merely because the system proposed them.

The central ambition is controlled evolution through observable, testable, reversible changes.

## What controlled evolution includes

The system's vocabulary of cognitive roles is not fixed at design time. Where recurring evidence shows a weakness that no existing role is shaped to address, the system may commission a new role and evaluate it like any other candidate change.

What actors should exist is therefore treated as a question for evidence rather than one to be answered in advance. Much else is deferred on the same reasoning: context governance, memory policy, model assignment, evaluation thresholds.

## What is not evolvable

That posture is only defensible because something sits beneath it.

A small, human-authored layer of goals, resource ceilings, and hard constraints is readable by every part of the system and writable by none. It is amended by direct human action, never by system proposal, however well evidenced, and it is enforced by a deterministic mechanism rather than merely stated.

Without such a floor, a system that adapts its own evaluation criteria can satisfy its own measurements by redefining what is being measured.

The floor and the deferral above are one position rather than two. Leaving things open is only safe where failure can be neither catastrophic nor self-concealing, and those are what the invariant layer and observability respectively provide.

## Success

Success means that fresh instances can start from accumulated system-level learning rather than repeatedly rediscovering the same workflow improvements.

Success also means that different models, orchestration strategies, context policies, and feedback architectures can be compared as whole-system configurations under reproducible conditions.

The strongest version of success is not a single "best" system. It is an environment capable of producing and evaluating multiple fit-for-purpose system generations.

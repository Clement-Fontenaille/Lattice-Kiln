# E1 — Can context pathology be detected from processing?

**Status:** not run.
**Gates:** nothing downstream depends on it; it feeds `10-foundations/04`'s failure
modes and M9's metric.

## The question

Whether a probe can distinguish a **constructed** context stress from its matched
control, using construction rather than outcome as the label. Outcome as a label would
make the probe a failure predictor wearing another name.

## The hypothesis is an ordering, not a cell

Fixed in writing before any data exists:

> calculus — contradiction > missing-context > overload > false-premise — chance

Two consequences follow from the hypothesis being the ordering. It **degrades
gracefully**: a weak apparatus shrinks every score while the ordering may survive. And
**the arm ranked last is the most informative** — false premise is the predicted null,
and a predicted null returning positive would overturn the structural-versus-semantic
boundary the whole account rests on.

## Design

One battery, not four experiments. Same apparatus, same model, same base tasks; five
stress classes with matched present/absent pairs.

**Calculus runs first as a positive control** and contributes no evidence about the
hypothesis. If the probe cannot detect arithmetic error, nothing downstream is
interpretable.

## What a null means — two different nulls

- **Everything near chance:** the apparatus is broken. Says nothing about context
  pathology.
- **Everything equal and above chance:** the probe detects *something is wrong*
  generically. That is a failure detector, not a pathology classifier, and the
  distinction matters because the four failure modes call for different responses.

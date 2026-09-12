# Notes — the context-management refoundation

**Date:** 2026-09-12
**Serves:** `23-arch-context-management/02-context-as-experimental-surface.md`, which this discussion produced; `23-arch-context-management/01-context-manager.md`, corrected on two points; `21-arch-knowledge-model/01` and `22-arch-cognition/04-thinking.md` on labelling; `22-arch-cognition/05-curation.md` on retention.

This file exists because the discussion that produced the refoundation contained more than the refoundation. Several points were raised that look secondary today and may not stay that way, and the instruction was explicit: record the initial reflection so the thread can be retraced and so positions can be refined later against what was actually said rather than against a summary of it.

The original draft is reproduced verbatim below, in the language it was written in. Nothing in it has been edited, including the parts the subsequent discussion revised.

---

## The initial draft, verbatim

> **Intention**
>
> Construire un framework expérimental permettant d'étudier différentes manières de représenter, retrouver et sélectionner le contexte nécessaire au fonctionnement d'un système agentique, sans figer prématurément l'architecture autour d'une technique particulière.
>
> L'objectif n'est pas de choisir a priori entre RAG, embeddings, recherche structurelle ou sélection apprise, mais de disposer d'un environnement dans lequel ces hypothèses peuvent être implémentées, combinées, instrumentées et comparées expérimentalement.
>
> **Contexte**
>
> Le système conserve un graphe persistant représentant les artefacts produits au cours de son fonctionnement : questions, hypothèses, observations, arguments, conclusions, décisions, sources, résultats d'expériences, etc., ainsi que les relations explicites permettant de retracer leur provenance et leur enchaînement logique.
>
> Chaque nouvel artefact peut être caractérisé par une représentation vectorielle. Il est également envisageable de conserver une représentation vectorielle du contexte dans lequel cet artefact a été produit.
>
> Cela ouvre la possibilité de retrouver non seulement des artefacts similaires à une requête, mais également des situations ou des états informationnels similaires à l'état courant du système, sans devoir conserver en permanence l'intégralité des contextes de production.
>
> Les liens explicites du graphe restent alors le mécanisme permettant, lorsqu'il est nécessaire de l'examiner, de reconstruire précisément le cheminement ayant conduit à un artefact.
>
> **Enjeu**
>
> La question centrale devient celle de la sélection initiale du contexte : étant donné l'état courant d'une tâche et l'ensemble des connaissances accumulées, quels artefacts faut-il consulter ?
>
> Cette question est distincte de l'exploitation de la topologie du graphe une fois qu'un artefact a été sélectionné.
>
> Le framework doit donc permettre d'expérimenter différents mécanismes de représentation et de sélection, et surtout d'étudier leur interaction avec le modèle chargé du raisonnement.
>
> **Voies à explorer**
>
> Plusieurs stratégies peuvent être rendues interchangeables.
>
> *Représentation des artefacts*
> - modèle d'embedding dédié ;
> - représentations produites par le modèle de raisonnement lui-même, par exemple à partir de ses états internes ;
> - différentes sérialisations d'un même artefact ;
> - représentations combinant contenu, type, métadonnées et contexte de production.
>
> *Représentation du contexte*
> - embedding du contenu effectivement fourni au modèle ;
> - représentation agrégée des artefacts présents ;
> - embedding d'épisodes ou de situations complètes ;
> - représentations hiérarchiques permettant de retrouver d'abord une situation puis ses artefacts constitutifs.
>
> *Politiques de sélection*
> - recherche sémantique classique ;
> - recherche par similarité avec le contexte courant ;
> - combinaison de plusieurs signaux ;
> - sélection apprise à partir des trajectoires observées ;
> - sélection itérative, dans laquelle chaque nouvelle production modifie l'état à partir duquel la recherche suivante est effectuée ;
> - politiques expérimentales exploitant conjointement représentations vectorielles et structure du graphe.
>
> *Modèles*
>
> Ces mécanismes doivent pouvoir être testés avec différents modèles locaux, indépendamment les uns des autres. Il devient ainsi possible de comparer, par exemple, un modèle d'embedding spécialisé avec les représentations internes du modèle agentique lui-même.
>
> **Instrumentation expérimentale**
>
> Chaque sélection doit être enregistrée comme une décision expérimentale à part entière : candidats considérés, scores, représentation utilisée, budget, éléments sélectionnés, contexte effectivement transmis au modèle et conséquences observées.
>
> La collecte des transitions et mutations du système permet ensuite de comparer les politiques non seulement sur leur résultat final, mais également sur les trajectoires qu'elles produisent.
>
> On peut notamment étudier quels artefacts ont effectivement contribué aux résultats obtenus, et utiliser ces observations comme signal pour de futures politiques de sélection.
>
> **Perspectives**
>
> Une telle architecture permettrait progressivement de passer d'un simple mécanisme de retrieval à un véritable laboratoire expérimental du context management.
>
> Le framework pourrait notamment permettre d'étudier si :
> - l'espace vectoriel d'un modèle d'embedding dédié est plus utile que celui du modèle agentique ;
> - un contexte passé peut être retrouvé directement comme une situation analogue ;
> - la représentation du contexte de production apporte davantage que la représentation isolée des artefacts ;
> - les trajectoires observées permettent d'apprendre une politique de sélection ;
> - les différentes stratégies dépendent fortement du modèle, de la tâche ou du budget disponible ;
> - une politique de sélection peut être apprise indépendamment du modèle de raisonnement.
>
> L'enjeu à terme est donc moins de concevoir un context manager que de construire l'infrastructure permettant de déterminer expérimentalement quelles représentations et quelles politiques permettent effectivement de retrouver le contexte utile, dans quelles conditions, et avec quel coût.

---

## Questions posed alongside the draft, not yet answered

These were raised in the same message and are recorded because they are open, not because they were resolved.

**Caching and what survives a request.** What remains of a request and of the generation that follows it? Must context be re-ingested on every request, or can persistence and caching accelerate context management when tasks follow one another? The part of this that was answered is in `01-context-manager.md` under Prefix persistence; the rest is not.

**The ontology's inventory.** The claim vocabulary proposed for the knowledge base appears to fit the stated objectives, but the precise inventory of its terms still has to survive design scrutiny: who assigns these labels, on the basis of what methodology. This was named as something that should stop the project for a while rather than be passed over.

**Indexing and selection of what lives in the knowledge base.** The necessity of explicitly managing the live set is correctly identified, but the precise forms of indexing and of selecting knowledge-base material to bring back into context can be questioned and enriched.

## Positions taken in the discussion that followed

Recorded compactly. Each is either written into a document or explicitly deferred.

**Recall is the positive operation.** It means bringing an element back in front of the model, not withholding one. An earlier reading here had it backwards. Written into `01-context-manager.md`.

**Prefix persistence changes the shape of the strategy space, not only its cost.** Without it, the whole live set is recalled every turn by necessity and the only remaining lever is presentation order. With it, the space opens and becomes much less settled — what belongs in the stable prefix, whether anything is ever removed from it, what happens when something dropped must return. Those need experiment and whatever the literature already holds. Written into `01-context-manager.md`.

**Adopt the framing, the instrumentation and the interchangeable interface; adopt none of the techniques.** Written into `02-context-as-experimental-surface.md`.

**Attribution is elided deliberately.** Determining which artifacts contributed to a result is credit assignment and is hard at small N. The position is to rely on aggregate comparison and hope not to have to solve it explicitly. Recorded with its risk in `02`.

**Labelling has a recursion problem.** See below — this is the one position that changed an actor's responsibilities.

**Forgetting has two parts, and only one has been addressed.** The transition from discussion to memory is what `22-arch-cognition/05-curation.md` describes. Retention *within* memory is a second question: the project's textual content cannot grow indefinitely, and hierarchy is there to help find what matters rather than to make unbounded growth acceptable. Named in `05-curation.md`, not addressed.

**The model's capacity to filter what passes from discussion to memory is central**, and the mechanisms the context manager implements are a system prerogative that the feedback loops must be able to inspect and adjust.

**Policy adequacy is model-dependent.** The evidence is immediate and local: this project is currently operated by hand as a knowledge base, without a context manager, by a model capable enough not to need one, and a less capable model manifestly cannot do it. That implies a gradient of adequate policies indexed by model rather than one correct policy. Written into `02`.

**Specific training may be what unlocks leverage from the knowledge base**, and if so the trade it enables is disk space for context space. Recorded as a direction in `02`, with nothing acting on it.

## On labelling, and why the thinking family is not the answer

This pass had proposed that a member of the thinking family assigns `03`'s labels — claim type, source, mode of acquisition, scope. That was rejected on a specific ground worth preserving.

Interactions with the model *are* the discussion. Explicitly invoking the model to label artifacts is not out of the question, but it poses a difficult recursion: the labelling call is itself a crossing, producing an artifact, which is itself material that would need labelling. Nothing in the design stops that regress on its own.

Two escapes were named, and neither is adopted yet.

- **Inline.** Ask the producing model to format its responses so that labels and relations are carried in the output itself. No separate call, so no regress — the labelling is a property of how the discussion is written down rather than an operation performed on it afterwards.
- **Out of band.** Use a different model, smaller and more specialised, to do the labelling. Its calls are not part of the discussion being labelled, so the regress does not close.

The two differ in more than mechanism. Inline labelling makes label quality a function of the reasoning model's compliance with a format, and couples it to whatever that model is. Out-of-band labelling makes it a separate capability that can be evaluated, replaced and trained independently — which fits the interchangeable-model axis in `02` — at the cost of a second model that never sees the reasoning that produced what it is labelling.

The methodology question sits underneath both and is unanswered either way. `90-notes/02` F6 is the relevant prior result: mode of acquisition turned out to be assessed **per link of a claim's provenance chain**, not once for the claim as a whole. That was found by a hand-tagging trial against the real corpus, and no specification written in advance would have caught it. The same approach — run the trial by hand with the current vocabulary before deciding whether anything can be automated — is the cheapest way to find the next such result.

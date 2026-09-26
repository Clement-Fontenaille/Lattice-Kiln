# Base de réflexion --- conception d'un environnement Harness / Agent Runtime

> Document de synthèse issu des itérations de réflexion menées dans
> cette conversation.
>
> **Objectif :** constituer une base de travail réutilisable pour les
> prochaines itérations de développement et d'expérimentation d'un
> environnement de harness pour agents de développement logiciel.
>
> **État des connaissances :** septembre 2026. Les points décrivant
> OpenCode, Cline et Qwen doivent être considérés comme des constats
> d'architecture à revalider au fil de l'évolution rapide de ces
> projets.

------------------------------------------------------------------------

## 0. Résumé exécutif

L'orientation qui se dégage des échanges est la suivante :

**Un harness moderne ne devrait pas être pensé comme un simple "chat +
outils + compaction".**

Le véritable objet intéressant est un **runtime d'agent avec une couche
explicite de gestion du contexte**, capable de distinguer :

1.  l'historique canonique de la session ;
2.  le contexte effectivement projeté vers le modèle pour un appel donné
    ;
3.  les informations récupérables mais non présentes dans le contexte
    courant ;
4.  les capacités/outils disponibles ;
5.  les sous-contextes d'agents spécialisés ;
6.  la mémoire persistante ;
7.  les règles/configurations partagées ;
8.  les politiques d'organisation ;
9.  les mécanismes de compression/compaction ;
10. le routage vers différents modèles.

La conclusion importante sur la question RAG est :

> **La "RAG au niveau de la projection de contexte" existe réellement
> dans les harness open source actuels. Ce n'est pas une idée purement
> théorique. En revanche, elle est généralement exposée comme un point
> d'extension du runtime plutôt que fournie comme un gestionnaire
> sémantique de contexte complet et générique.**

OpenCode et Cline fournissent aujourd'hui des points d'ancrage
particulièrement nets pour cela :

-   OpenCode possède un hook `context` exécuté immédiatement avant le
    dispatch d'un appel modèle, capable de modifier système, messages,
    outils et options de requête.
-   Cline possède un `beforeModel` hook et un pipeline de contexte, avec
    séparation explicite entre transcript canonique, projection et
    compaction.

Cela permet de construire une architecture du type :

``` text
                 ┌─────────────────────────────┐
                 │     Session canonique       │
                 │ transcript / artefacts      │
                 └──────────────┬──────────────┘
                                │
                                ▼
                 ┌─────────────────────────────┐
                 │ Context Manager / Projector │
                 │                             │
                 │ - budget tokens             │
                 │ - pertinence                │
                 │ - mémoire                   │
                 │ - RAG                       │
                 │ - skills                    │
                 │ - état de tâche             │
                 │ - sélection outils          │
                 └──────────────┬──────────────┘
                                │
                                ▼
                 ┌─────────────────────────────┐
                 │ Context effectif du modèle │
                 │ system + messages + tools  │
                 └──────────────┬──────────────┘
                                │
                                ▼
                              LLM
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                  tools                  réponse
                    │
                    ▼
          filesystem / MCP / APIs / etc.
```

Le **MCP** doit être positionné différemment :

> **MCP est une couche d'accès/capacité, pas une couche de gestion du
> contexte.**

Il définit comment le harness peut exposer au modèle des outils,
ressources et autres primitives externes. Il ne décide pas, à lui seul,
de ce qui est pertinent, de ce qui doit être injecté, ni de la manière
de respecter un budget de contexte.

La séparation conceptuelle à conserver est donc :

``` text
MCP          = comment accéder
RAG          = quoi retrouver
Context Mgmt = quoi exposer maintenant
Compaction   = comment réduire / synthétiser
Memory       = quoi conserver entre les appels/sessions
Subagents    = où déporter un contexte de travail
Harness      = qui orchestre tout cela
```

------------------------------------------------------------------------

# 1. Question centrale du projet

Le problème n'est pas seulement :

> "Comment donner plus de contexte à un LLM ?"

Mais plutôt :

> **"Comment construire un runtime capable de présenter dynamiquement au
> modèle le bon sous-ensemble de l'état global disponible, au bon
> moment, avec le bon budget, sans perdre la continuité de la tâche ?"**

Cela implique de séparer au minimum :

``` text
                    GLOBAL STATE
                         │
          ┌──────────────┼────────────────┐
          │              │                │
          ▼              ▼                ▼
       Memory        Workspace         Session
          │              │                │
          │              │                ▼
          │              │          Canonical history
          │              │                │
          └──────────────┼────────────────┘
                         │
                         ▼
                Context Projection
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          System      Messages      Tools
             │           │           │
             └───────────┼───────────┘
                         ▼
                        LLM
```

La difficulté architecturale principale est donc la **projection**.

------------------------------------------------------------------------

# 2. Les quatre grandes familles de mécanismes identifiées

## 2.1 Tool-call RAG

Le modèle dispose d'un outil du type :

``` text
search_code(query)
search_docs(query)
search_memory(query)
search_issue_tracker(query)
```

Il décide lui-même quand rechercher.

Pipeline :

``` text
LLM
 │
 ├── tool_call(search(...))
 │
 ▼
Harness
 │
 ▼
Retriever / DB / filesystem / API
 │
 ▼
tool_result
 │
 ▼
LLM
```

### Avantages

-   architecture simple ;
-   comportement facilement observable ;
-   le modèle contrôle la récupération ;
-   bonne compatibilité avec les agents existants ;
-   très naturel avec MCP.

### Limites

Le résultat devient généralement un élément du contexte de conversation.

Donc :

``` text
search
→ gros résultat
→ contexte augmente
→ nouveau tool call
→ nouveau résultat
→ contexte augmente
```

La qualité de sélection dépend alors fortement du modèle et de la
discipline de l'agent.

------------------------------------------------------------------------

# 3. RAG via MCP

MCP doit être considéré comme un **protocole de capacité / accès**, pas
comme un moteur RAG.

Un serveur MCP peut fournir notamment :

-   tools ;
-   resources ;
-   prompts / instructions selon implémentation ;
-   accès à des bases de données ;
-   APIs ;
-   systèmes internes ;
-   services spécialisés.

Pipeline typique :

``` text
                 Harness
                    │
                    ▼
                 MCP layer
              ┌─────┴─────┐
              ▼           ▼
            Tools       Resources
              │           │
              ▼           ▼
           external     external
           systems      knowledge
```

### MCP Tool

Le modèle demande :

``` text
call search(...)
```

Le harness exécute le tool.

Le résultat revient dans le contexte.

### MCP Resource

Une ressource est plutôt une information adressable et lisible.

Conceptuellement :

``` text
resource://repo/module-x/design.md
```

Le harness/modèle peut demander à la lire.

Le contenu devient alors disponible dans le contexte.

### Point architectural important

MCP ne répond pas à :

> "Quelle ressource faut-il sélectionner maintenant ?"

Il répond principalement à :

> "Comment accéder à cette capacité ou cette ressource ?"

La décision de pertinence reste du côté :

-   du modèle ;
-   du harness ;
-   d'un retriever ;
-   d'un context manager ;
-   ou d'une combinaison des quatre.

------------------------------------------------------------------------

# 4. RAG au niveau de la projection de contexte

C'est le point le plus intéressant pour le projet.

Le runtime possède un contexte canonique :

``` text
C = history + state + memory + workspace + tools + policies
```

Avant chaque appel au modèle, il calcule :

``` text
P(C, task, budget, policy) → C_effective
```

où `P` est une fonction de projection.

Le modèle ne voit donc pas nécessairement tout `C`.

Il voit :

``` text
C_effective ⊂ C
```

### Exemple

Le runtime connaît :

``` text
- 1000 messages historiques
- 300 fichiers indexés
- 80 décisions de projet
- 50 entrées mémoire
- 12 MCP servers
- 100 tools
- 30 skills
- 4 agents spécialisés
```

Mais pour le prochain appel il ne présente que :

``` text
SYSTEM
+ tâche actuelle
+ état courant
+ 3 décisions pertinentes
+ 2 fichiers pertinents
+ 1 skill
+ 5 tools
+ résultat synthétique d’un subagent
```

Le contexte envoyé au modèle reste petit alors que l'état global peut
être immense.

------------------------------------------------------------------------

# 5. Est-ce une idée expérimentale ou une architecture réellement utilisée ?

## Réponse

**L'architecture existe déjà dans les harness OSS.**

Mais il faut distinguer deux affirmations :

### Affirmation A --- "Les runtime OSS fournissent des points d'extension pour projeter/modifier le contexte juste avant l'appel modèle."

Oui.

### Affirmation B --- "Les harness OSS possèdent déjà un Context Manager sémantique complet, générique, qui comprend les faits, décisions, artefacts, pertinence et budgets."

Beaucoup moins.

Le paysage actuel est plutôt :

``` text
                 maturité
                    │
                    ▼

Tool RAG       ██████████
MCP tools     ██████████
Compaction    ██████████
Skills        █████████
Subagents     █████████
Context hooks ████████
Memory        ███████
Semantic CM   ████
```

La dernière catégorie est précisément l'espace où il semble pertinent
d'expérimenter.

------------------------------------------------------------------------

# 6. OpenCode comme point d'ancrage

OpenCode est particulièrement intéressant parce que son architecture
expose explicitement un hook :

``` text
session.hook("context", ...)
```

Ce hook intervient **immédiatement avant le dispatch d'une requête au
modèle**.

Il peut modifier :

-   system instructions ;
-   messages ;
-   tools ;
-   request options.

C'est exactement le seam nécessaire pour construire un context projector
externe/interne.

Conceptuellement :

``` text
Canonical session
       │
       ▼
OpenCode context assembly
       │
       ▼
context hook
       │
       ├── retrieve memory
       ├── retrieve docs
       ├── retrieve project state
       ├── select tools
       ├── inject skill
       ├── remove irrelevant context
       └── enforce token budget
       │
       ▼
Model request
```

Point crucial :

> La modification opérée par le hook concerne le contexte de l'appel
> sortant et ne doit pas être confondue avec une modification de
> l'historique canonique persistant.

Cela donne une séparation extrêmement utile :

``` text
durable state ≠ effective context
```

OpenCode possède également un hook distinct de `compaction`, ce qui
confirme la séparation conceptuelle :

``` text
context projection
        ≠
compaction/checkpoint
```

Source officielle : https://opencode.ai/v2/docs/build/plugins

------------------------------------------------------------------------

# 7. Cline comme point d'ancrage

L'évolution actuelle de Cline est particulièrement intéressante pour ce
projet.

Le SDK est maintenant explicitement organisé en couches :

``` text
@cline/shared
      │
      ├── contracts
      ├── hooks
      └── extensions
            │
            ▼
@cline/llms
            │
            ▼
@cline/agents
            │
            ▼
@cline/core
            │
            ▼
Host applications
```

`@cline/agents` possède le runtime loop et expose notamment :

``` text
beforeRun
beforeModel
afterModel
beforeTool
afterTool
afterRun
...
```

Le `beforeModel` hook permet notamment :

> Inject context, last-mile prompt edits.

`@cline/core`, de son côté, possède :

-   orchestration stateful ;
-   sessions ;
-   persistence ;
-   config ;
-   plugins ;
-   context pipeline ;
-   compaction policy.

L'architecture distingue explicitement :

``` text
canonical transcript
        │
        ▼
context / turn preparation
        │
        ▼
projection
        │
        ▼
provider call
```

et conserve la compaction dans une couche dédiée.

Cette évolution est particulièrement pertinente pour le projet car elle
montre que le "context pipeline" est en train de devenir une **primitive
architecturale explicite du runtime**, plutôt qu'un simple détail du
prompt builder.

Sources officielles :

https://github.com/cline/cline/blob/main/sdk/ARCHITECTURE.md

https://github.com/cline/cline/blob/main/sdk/packages/agents/README.md

https://github.com/cline/cline/blob/main/sdk/packages/core/README.md

------------------------------------------------------------------------

# 8. Qwen Code comme autre référence

Qwen Code est particulièrement intéressant pour une autre raison : il
pousse davantage les concepts de :

-   skills ;
-   subagents ;
-   mémoire ;
-   team memory ;
-   auto-memory ;
-   auto-skill ;
-   MCP resources ;
-   orchestration de plusieurs modèles.

Le pattern intéressant est :

``` text
                 Qwen Code
                     │
       ┌─────────────┼──────────────┐
       ▼             ▼              ▼
    Skills        Memory           MCP
       │             │              │
       ▼             ▼              ▼
 progressive      retrieval      tools/resources
 disclosure
       │
       └─────────────┬──────────────┘
                     ▼
                model context
```

Qwen permet notamment l'utilisation explicite de ressources MCP dans le
contexte.

Cela constitue un autre exemple de la séparation :

``` text
resource access
       ↓
context inclusion
```

Le projet de harness peut donc étudier Qwen comme référence pour la
partie :

> "Comment enrichir progressivement un contexte avec mémoire, skills et
> ressources externes ?"

------------------------------------------------------------------------

# 9. Skills : une forme spécialisée de RAG

Une conclusion importante de la conversation est que les **skills**
peuvent être compris comme une forme de retrieval contrôlé.

Un skill n'est pas nécessairement chargé entièrement au démarrage.

Pattern :

``` text
Skill registry
     │
     ▼
metadata / description
     │
     ▼
relevance detection
     │
     ▼
skill selected
     │
     ▼
load detailed instructions
```

Cela correspond à :

``` text
progressive disclosure
```

plutôt qu'à :

``` text
load everything
```

Cette approche est très importante pour éviter le "context stuffing".

Elle est applicable non seulement aux instructions, mais aussi :

-   aux conventions de code ;
-   aux procédures d'exploitation ;
-   aux APIs internes ;
-   aux connaissances métier ;
-   aux politiques ;
-   aux playbooks ;
-   aux architectures ;
-   aux standards d'équipe.

------------------------------------------------------------------------

# 10. Subagents : un mécanisme de partition du contexte

Les subagents ne servent pas uniquement à paralléliser le travail.

Ils servent aussi à **isoler le contexte de travail**.

Sans subagent :

``` text
Main agent
  │
  ├── recherche 100 fichiers
  ├── analyse architecture
  ├── explore tests
  ├── inspect issues
  └── raisonne
       │
       ▼
  énorme contexte
```

Avec subagent :

``` text
Main agent
  │
  ├──► Research agent
  │       └── 100 fichiers
  │       └── synthèse
  │
  ├──► Test agent
  │       └── tests
  │       └── synthèse
  │
  └──► Architecture agent
          └── analyse
          └── synthèse
                │
                ▼
          Main context
```

Le parent reçoit seulement :

``` text
synthèse
+ références pertinentes
+ conclusions
+ artefacts
```

C'est une forme très efficace de **context partitioning**.

Le contexte total consommé par le système peut être grand, mais le
contexte du parent reste contrôlé.

------------------------------------------------------------------------

# 11. Compaction : nécessaire mais insuffisante

Le modèle classique est :

``` text
history
   │
   ▼
token overflow
   │
   ▼
compaction
   │
   ▼
summary
   │
   ▼
continue
```

Cela fonctionne, mais c'est une stratégie essentiellement **réactive**.

Elle répond à :

> "Le contexte est devenu trop gros."

Elle ne répond pas forcément à :

> "Quelles informations devraient être présentes maintenant ?"

La projection de contexte apporte une deuxième dimension :

``` text
Compaction = compression temporelle
Projection = sélection contextuelle
```

On peut donc imaginer :

``` text
                 Context Manager
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Projection            Compaction
        “quoi montrer”         “quoi résumer”
```

Les deux doivent être complémentaires.

------------------------------------------------------------------------

# 12. Canonical history vs effective context

Cette distinction est probablement l'un des invariants architecturaux
les plus importants à préserver.

## Canonical history

C'est la source de vérité :

``` text
messages
tool calls
tool results
events
artifacts
state transitions
```

Elle sert à :

-   reprendre une session ;
-   auditer ;
-   déboguer ;
-   reconstruire l'état ;
-   générer une compaction ;
-   produire des métriques.

## Effective context

C'est une projection temporaire :

``` text
system
+ selected history
+ selected memory
+ selected files
+ selected skills
+ selected tools
+ selected MCP resources
```

Elle sert uniquement à un appel modèle donné.

Donc :

``` text
Canonical State
      │
      │ projection
      ▼
Effective Context
      │
      ▼
LLM
```

Ne pas fusionner ces deux concepts est probablement essentiel à la
robustesse du futur harness.

------------------------------------------------------------------------

# 13. Le modèle mental proposé pour le futur harness

Une architecture cible possible :

``` text
┌──────────────────────────────────────────────────────────┐
│                    HARNESS RUNTIME                       │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │                  Session Manager                   │  │
│  │                                                    │  │
│  │  canonical history / state / artifacts             │  │
│  └───────────────────────┬────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │                 Context Manager                    │  │
│  │                                                    │  │
│  │  1. task state                                     │  │
│  │  2. relevant history                               │  │
│  │  3. memory retrieval                               │  │
│  │  4. RAG                                            │  │
│  │  5. skills                                         │  │
│  │  6. MCP resources                                  │  │
│  │  7. subagent outputs                               │  │
│  │  8. tool selection                                 │  │
│  │  9. token budget                                   │  │
│  │ 10. compaction state                               │  │
│  └───────────────────────┬────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Model Request Builder                 │  │
│  │                                                    │  │
│  │ system + messages + tools + options                │  │
│  └───────────────────────┬────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│                     Model Router                        │
│                          │                               │
│             ┌────────────┼────────────┐                 │
│             ▼            ▼            ▼                 │
│          strong       cheap        specialist            │
│           model        model          model              │
│                                                          │
└──────────────────────────────────────────────────────────┘
             │                  │                 │
             ▼                  ▼                 ▼
           Tools              MCP              Subagents
             │                  │                 │
             ▼                  ▼                 ▼
         filesystem        external         isolated
         shell             systems          contexts
         git               resources        / models
```

------------------------------------------------------------------------

# 14. Où placer MCP dans cette architecture ?

Le point important est de **ne pas faire de MCP le Context Manager**.

Une séparation saine :

``` text
                    Context Manager
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
      Memory             RAG              MCP
        │                 │                 │
        │                 │                 ├── tools
        │                 │                 └── resources
        │                 │
        └─────────────────┴─────────────────┘
                          │
                          ▼
                  Context Projection
```

MCP est alors une source de capacités/connaissances parmi d'autres.

------------------------------------------------------------------------

# 15. MCP tools vs MCP resources

## Tools

Ils sont généralement adaptés à :

-   action ;
-   recherche ;
-   interrogation ;
-   transformation ;
-   exécution.

Exemple :

``` text
searchLinearIssues()
queryDatabase()
getGithubPR()
runDeploymentCheck()
```

Ils ont naturellement un coût contextuel :

``` text
tool schema
+
tool call
+
tool result
```

Plus le nombre de tools exposés augmente, plus le contexte peut devenir
coûteux.

------------------------------------------------------------------------

## Resources

Elles sont adaptées à :

-   documents ;
-   état ;
-   connaissances ;
-   artefacts ;
-   ressources adressables.

Pattern :

``` text
resource URI
       │
       ▼
read
       │
       ▼
content
       │
       ▼
context
```

Elles sont particulièrement intéressantes pour une architecture de
projection de contexte.

------------------------------------------------------------------------

# 16. Le problème des MCP servers nombreux

Un anti-pattern potentiel :

``` text
100 MCP servers
      │
      ▼
1000 tools
      │
      ▼
énorme tool schema
      │
      ▼
context cost
```

Le futur harness pourrait donc introduire :

``` text
Capability Discovery
       │
       ▼
Relevant MCP servers
       │
       ▼
Relevant tools/resources
       │
       ▼
Effective toolset
       │
       ▼
LLM
```

Autrement dit :

> **Ne pas seulement router les requêtes ; router également les
> capacités.**

Cela ouvre une piste très intéressante :

``` text
Capability RAG
```

où le runtime récupère les capacités pertinentes avant de les présenter
au modèle.

------------------------------------------------------------------------

# 17. Multi-model orchestration

Les quatre harness étudiés ne sont pas équivalents sur ce point.

Le modèle conceptuel utile est :

``` text
                 Task
                  │
                  ▼
             Orchestrator
                  │
       ┌──────────┼───────────┐
       ▼          ▼           ▼
   planner      coder       reviewer
       │          │           │
       ▼          ▼           ▼
    model A     model B     model C
```

Le point important est que le routage modèle peut être fait à plusieurs
niveaux :

### Niveau session

Un modèle principal pour toute la tâche.

### Niveau agent

Chaque subagent possède son modèle.

### Niveau appel

Le runtime peut potentiellement choisir un modèle selon :

-   coût ;
-   complexité ;
-   latence ;
-   type d'opération ;
-   criticité.

### Niveau outil

Certaines opérations peuvent utiliser un modèle spécialisé.

------------------------------------------------------------------------

# 18. OpenCode / Cline / Qwen / Gemini : comparaison conceptuelle

  ----------------------------------------------------------------------------------
  Capacité       OpenCode           Cline            Qwen Code       Gemini CLI
  -------------- ------------------ ---------------- --------------- ---------------
  Skills         Oui                Oui              Oui             Oui

  Progressive    Oui                Oui              Oui             Oui
  disclosure                                                         

  Subagents      Oui                Oui              Oui             Oui

  Context        Oui                Oui              Oui             Oui
  compaction                                                         

  Context hook / Très explicite     Très explicite   Hooks           Hooks
  projection                        dans SDK         disponibles     disponibles
  seam                                                               

  MCP tools      Oui                Oui              Oui             Oui

  MCP resources  Oui dans           Oui /            Oui,            Oui selon
                 l'implémentation   intégration MCP  explicitement   intégration
                 actuelle                            utilisables     

  Mémoire        Extensions /       Session/team     Auto-memory /   mécanismes de
  persistante    mécanismes du      state et         team-memory     mémoire selon
                 runtime            extensions                       configuration

  Multi-model    Oui                Oui              Oui             Oui

  Organisation / Très forte         forte avec       forte           forte
  config                            SDK/hub/config                   
  centralisée                       management                       

  Architecture   Très forte         Très forte via   forte           forte
  runtime                           SDK                              
  extensible                                                         
  ----------------------------------------------------------------------------------

Cette table ne doit pas être interprétée comme un classement.

Les quatre projets ont des philosophies différentes.

------------------------------------------------------------------------

# 19. Ce que Cline est devenu architecturalement

Un point à ne pas perdre dans les expérimentations :

Cline n'est plus seulement à considérer comme une extension IDE.

Son SDK expose désormais :

``` text
@cline/sdk
@cline/core
@cline/agents
@cline/llms
@cline/shared
```

avec :

-   runtime loop ;
-   tools ;
-   hooks ;
-   teams ;
-   MCP ;
-   sessions ;
-   persistence ;
-   hub ;
-   remote config ;
-   context pipeline.

Cela en fait une référence intéressante pour étudier comment construire
un **runtime de harness programmable**, indépendamment de l'UI.

------------------------------------------------------------------------

# 20. Configuration partagée / environnement organisationnel

La question de l'environnement partagé est différente de la simple
configuration utilisateur.

Il faut distinguer :

``` text
User config
Project config
Organization config
Managed policy
Runtime state
```

Une architecture robuste :

``` text
                 Organization
                      │
                 Managed Policy
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Project config          User config
          │                       │
          └───────────┬───────────┘
                      ▼
                Effective config
                      │
                      ▼
                  Harness
```

La configuration effective doit être le résultat d'une résolution
déterministe :

``` text
managed
  >
organization
  >
project
  >
user
  >
session override
```

ou d'une politique équivalente explicitement définie.

Il faut éviter le mélange implicite entre :

-   configuration ;
-   contexte ;
-   mémoire ;
-   policy ;
-   prompt.

------------------------------------------------------------------------

# 21. Pourquoi la configuration organisationnelle est importante

Dans un environnement partagé, il ne suffit pas de partager un fichier
`.rules`.

Il faut pouvoir contrôler :

-   modèles autorisés ;
-   MCP servers autorisés ;
-   tools autorisés ;
-   skills obligatoires ;
-   skills interdits ;
-   politiques de sécurité ;
-   prompts système ;
-   budgets ;
-   limites de coût ;
-   providers ;
-   credentials / secrets ;
-   règles de conformité ;
-   télémétrie ;
-   mémoire partagée ;
-   conventions d'équipe.

On passe donc de :

``` text
dotfiles partagés
```

à :

``` text
managed runtime policy
```

Cette distinction est importante pour le projet.

------------------------------------------------------------------------

# 22. OpenCode, Cline, Qwen, Gemini sur la question organisationnelle

### OpenCode

Particulièrement intéressant pour :

-   config globale ;
-   config projet ;
-   configuration gérée/organisationnelle ;
-   politiques ;
-   plugins ;
-   runtime extensible.

### Cline

Intéressant pour :

-   SDK ;
-   hub ;
-   remote config ;
-   runtime partagé ;
-   config watchers ;
-   plugins ;
-   contexte.

Son architecture actuelle montre qu'il peut servir de base à un
environnement partagé, notamment via son abstraction Hub.

### Qwen Code

Intéressant pour :

-   configuration système ;
-   configuration projet ;
-   mémoire d'équipe ;
-   skills ;
-   MCP ;
-   multi-agent.

### Gemini CLI

Intéressant pour :

-   policies administratives ;
-   configuration système ;
-   contrôle des capacités ;
-   intégration forte avec l'écosystème Gemini.

------------------------------------------------------------------------

# 23. Un environnement partagé devrait distinguer quatre plans

Une architecture utile :

``` text
┌─────────────────────────────────────┐
│           CONTROL PLANE             │
│                                     │
│ policies                            │
│ org config                          │
│ model routing policy                │
│ MCP allowlist                       │
│ skill registry                      │
│ security                            │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          KNOWLEDGE PLANE            │
│                                     │
│ docs                                │
│ memory                              │
│ embeddings                          │
│ project knowledge                   │
│ indexed repositories                │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           RUNTIME PLANE             │
│                                     │
│ sessions                            │
│ agents                              │
│ subagents                           │
│ tools                               │
│ MCP                                 │
│ context projection                  │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           MODEL PLANE               │
│                                     │
│ model router                        │
│ providers                           │
│ quotas                              │
│ fallback                            │
└─────────────────────────────────────┘
```

Cette séparation paraît particulièrement pertinente pour éviter de
transformer le harness en gros "prompt builder".

------------------------------------------------------------------------

# 24. Architecture proposée pour un Context Manager

Le futur composant pourrait être explicitement modélisé comme :

``` typescript
interface ContextManager {
  prepare(request: ContextRequest): Promise<EffectiveContext>
}
```

Avec :

``` typescript
interface ContextRequest {
  sessionId: string
  task: TaskState
  canonicalState: SessionState
  tokenBudget: TokenBudget
  model: ModelDescriptor
  capabilities: CapabilitySet
  policy: ContextPolicy
}
```

et :

``` typescript
interface EffectiveContext {
  system: ContextBlock[]
  messages: Message[]
  tools: ToolDefinition[]
  resources: ResourceReference[]
  metadata: ContextMetadata
}
```

Le Context Manager pourrait appeler :

``` text
MemoryProvider
KnowledgeProvider
SkillProvider
MCPProvider
ArtifactProvider
HistoryProvider
SubagentProvider
CapabilityProvider
```

------------------------------------------------------------------------

# 25. Une architecture de retrieval plus générale

Au lieu de :

``` text
RAG(query) → chunks
```

penser :

``` text
ContextQuery
    │
    ├── semantic relevance
    ├── temporal relevance
    ├── task relevance
    ├── dependency relevance
    ├── authority
    ├── freshness
    ├── user/org scope
    └── token cost
             │
             ▼
       Ranked candidates
             │
             ▼
       Budget allocator
             │
             ▼
       Context projection
```

Cela permettrait de considérer différents objets comme des candidats au
contexte :

``` text
Document
File
Code symbol
Memory
Decision
Issue
Skill
Tool
MCP resource
Subagent result
Artifact
Previous turn
```

Le retrieval devient donc un problème de **context selection**, pas
uniquement de recherche vectorielle.

------------------------------------------------------------------------

# 26. L'idée de "Context Objects"

Une piste de design particulièrement intéressante pour le futur harness
serait de normaliser les unités de contexte :

``` typescript
type ContextObject =
  | Document
  | CodeSymbol
  | Decision
  | Memory
  | Artifact
  | Skill
  | Tool
  | Resource
  | AgentResult
  | Message
```

Chaque objet pourrait posséder :

``` typescript
interface ContextObject {
  id: string
  type: ContextObjectType

  content?: string

  metadata: {
    source: string
    scope: string
    createdAt?: Date
    updatedAt?: Date
    authority?: number
    freshness?: number
    relevance?: number
  }

  tokenCost?: number
}
```

Le Context Manager pourrait alors raisonner sur :

``` text
relevance
+
authority
+
freshness
+
cost
+
scope
```

plutôt que sur une simple liste de messages.

C'est une évolution importante par rapport au modèle :

``` text
messages[] → prompt
```

------------------------------------------------------------------------

# 27. Attention à ne pas sur-architecturer trop tôt

Cette architecture est prometteuse, mais plusieurs éléments doivent
rester expérimentaux.

Il n'est pas nécessaire de construire immédiatement :

-   une ontologie complète ;
-   un knowledge graph ;
-   un vector DB obligatoire ;
-   une mémoire sémantique complexe ;
-   un planner hiérarchique ;
-   un système de scoring opaque.

Une progression raisonnable serait :

### Phase 1

``` text
canonical history
+
context projection hook
+
token budget
+
manual retrieval
```

### Phase 2

``` text
+ memory provider
+ file/code retrieval
+ skills retrieval
```

### Phase 3

``` text
+ MCP capability selection
+ resource retrieval
+ subagent result registry
```

### Phase 4

``` text
+ semantic ranking
+ adaptive budget allocation
+ automatic memory
```

### Phase 5

``` text
+ organization-level policy
+ multi-user shared knowledge
+ model routing
```

------------------------------------------------------------------------

# 28. Les primitives déjà "prouvées" par les harness existants

Il est raisonnable de considérer comme des primitives établies :

``` text
Tool calling
MCP
Skills
Progressive disclosure
Subagents
Parallel agents
Compaction
Context hooks
Persistent sessions
Model routing
Plugin systems
Config layering
Shared/managed configuration
```

Le fait qu'elles soient implémentées par plusieurs projets actifs
constitue un signal architectural fort.

Cela ne signifie pas que chaque primitive est optimale ni que son
efficacité empirique est universelle.

------------------------------------------------------------------------

# 29. Les éléments encore plus expérimentaux

Les pistes suivantes doivent être traitées comme des axes de R&D :

``` text
Semantic Context Manager
Dynamic context-object graph
Automatic relevance scoring
Capability RAG
Adaptive token allocation
Cross-agent memory synthesis
Automatic context provenance
Context quality evaluation
Context deduplication
Context freshness management
```

En particulier :

> Le concept de "context projection" est réel ; la question ouverte est
> plutôt **comment construire un projecteur sémantique qui soit meilleur
> que les mécanismes plus simples existants sans devenir imprévisible ou
> coûteux**.

------------------------------------------------------------------------

# 30. Critères d'évaluation à introduire dans les expérimentations

Pour éviter une architecture basée uniquement sur l'intuition, mesurer :

## Qualité

-   task success rate ;
-   regression rate ;
-   hallucination/error rate ;
-   missed-context rate ;
-   irrelevant-context rate.

## Contexte

-   input tokens ;
-   output tokens ;
-   tool-result tokens ;
-   context reuse ;
-   compaction frequency ;
-   context projection size.

## Coût

-   coût par tâche ;
-   coût par étape ;
-   coût des retrievals ;
-   coût des subagents ;
-   coût des appels MCP.

## Performance

-   latency ;
-   time-to-first-action ;
-   total wall-clock time ;
-   parallelism gain.

## Robustesse

-   session resume ;
-   compaction recovery ;
-   context corruption ;
-   stale memory ;
-   conflicting memory ;
-   MCP failure ;
-   model failure.

------------------------------------------------------------------------

# 31. Une métrique particulièrement intéressante : Context Efficiency

Une métrique utile pourrait être :

``` text
Context Efficiency =
useful context
----------------
total context
```

Avec une définition opérationnelle à construire.

Une autre :

``` text
Task Success / Input Tokens
```

ou :

``` text
Task Success / Total Cost
```

L'objectif n'est pas nécessairement de minimiser les tokens.

L'objectif est :

> **maximiser la quantité d'information utile par unité de
> contexte/coût.**

------------------------------------------------------------------------

# 32. Context provenance

Une capacité qui pourrait être très utile dans un environnement de
développement partagé :

Chaque fragment injecté devrait idéalement être traçable :

``` text
ContextBlock
   │
   ├── source
   ├── reason
   ├── retrieval query
   ├── relevance score
   ├── authority
   ├── timestamp
   └── token cost
```

Exemple :

``` text
[CONTEXT]
source = team-memory
id = decision-428
reason = relevant to current database migration
authority = organization
freshness = 0.92
cost = 180 tokens
```

Cela rend le système :

-   observable ;
-   débogable ;
-   auditable ;
-   optimisable.

------------------------------------------------------------------------

# 33. Une autre distinction essentielle : knowledge vs instructions

Le Context Manager devrait différencier :

``` text
Instructions
Knowledge
State
Evidence
Capabilities
```

Exemple :

``` text
Instruction:
"Use PostgreSQL migrations."

Knowledge:
"Database schema is in db/schema.sql."

State:
"Migration 014 is currently deployed."

Evidence:
"CI failed because column X is missing."

Capability:
"tool: run_migration"
```

Ces objets ne doivent pas forcément être injectés avec la même priorité.

------------------------------------------------------------------------

# 34. Policy vs Context

Dans un environnement partagé :

``` text
Policy
≠
Context
```

Une policy doit être considérée comme une contrainte du runtime.

Exemple :

``` text
policy:
  allowedModels = [...]
  allowedMcpServers = [...]
  maxContextTokens = ...
```

Le Context Manager ne devrait pas pouvoir "récupérer" une policy comme
s'il s'agissait d'une information ordinaire.

Elle doit être imposée par le runtime.

------------------------------------------------------------------------

# 35. Architecture multi-utilisateurs

Une session partagée introduit :

``` text
Organization
   │
   ├── user A
   ├── user B
   └── user C
          │
          ▼
      project
          │
          ▼
       sessions
```

Il faut distinguer :

``` text
org memory
team memory
project memory
user memory
session memory
```

et leurs scopes :

``` text
global
team
project
user
session
```

Le retrieval doit respecter le scope.

------------------------------------------------------------------------

# 36. Problème de confiance / autorité

Deux mémoires peuvent se contredire :

``` text
user memory:
  "Use Redis."

team memory:
  "Redis has been deprecated."

organization policy:
  "Redis is prohibited."
```

Le Context Manager doit donc avoir une hiérarchie d'autorité.

Par exemple :

``` text
policy
>
organization
>
team
>
project
>
user
>
session inference
```

La hiérarchie exacte reste un choix de conception.

Le point essentiel est qu'elle soit :

-   explicite ;
-   déterministe ;
-   observable.

------------------------------------------------------------------------

# 37. MCP et sécurité organisationnelle

MCP rend particulièrement importante la notion de :

``` text
capability policy
```

Exemple :

``` text
MCP server
   │
   ├── read repository
   ├── write repository
   ├── access production
   └── deploy
```

Le fait qu'un serveur existe ne signifie pas que tous ses tools doivent
être présentés au modèle.

Le futur harness pourrait donc introduire :

``` text
MCP server registry
        │
        ▼
policy filtering
        │
        ▼
capability retrieval
        │
        ▼
tool exposure
```

------------------------------------------------------------------------

# 38. Une architecture de pipeline complète

Architecture cible possible :

``` text
                  USER / EVENT
                       │
                       ▼
               ┌───────────────┐
               │ Session Layer │
               └───────┬───────┘
                       │
                       ▼
               ┌───────────────┐
               │ Task State    │
               └───────┬───────┘
                       │
                       ▼
             ┌────────────────────┐
             │ Context Manager    │
             │                    │
             │ retrieve           │
             │ rank               │
             │ filter             │
             │ budget             │
             │ project            │
             └─────────┬──────────┘
                       │
         ┌─────────────┼──────────────┐
         ▼             ▼              ▼
      Memory         RAG            Skills
         │             │              │
         └─────────────┼──────────────┘
                       │
                       ▼
                Capability Layer
                       │
              ┌────────┴─────────┐
              ▼                  ▼
             MCP               Tools
              │                  │
              └────────┬─────────┘
                       ▼
                Effective Context
                       │
                       ▼
                  Model Router
                       │
                       ▼
                      LLM
                       │
              ┌────────┴─────────┐
              ▼                  ▼
            Action             Answer
              │
              ▼
           Runtime
              │
              ▼
       canonical state update
```

------------------------------------------------------------------------

# 39. Ce qu'il ne faut probablement pas faire

## Anti-pattern 1 --- Tout mettre dans le prompt

``` text
README
+
all docs
+
all history
+
all tools
+
all skills
+
all memories
```

Cela transforme le contexte en cache global non contrôlé.

------------------------------------------------------------------------

## Anti-pattern 2 --- Tout mettre derrière des tools

Cela délègue toute la stratégie de retrieval au modèle.

------------------------------------------------------------------------

## Anti-pattern 3 --- Confondre MCP et RAG

MCP n'est pas un retriever.

------------------------------------------------------------------------

## Anti-pattern 4 --- Confondre compaction et context management

La compaction réduit l'historique.

Elle ne remplace pas une sélection dynamique des informations
pertinentes.

------------------------------------------------------------------------

## Anti-pattern 5 --- Faire du vector search l'unique intelligence

La pertinence d'un contexte peut dépendre de :

-   relations de code ;
-   autorité ;
-   temporalité ;
-   état ;
-   tâche ;
-   provenance ;
-   politique ;
-   dépendances.

Le score sémantique n'est qu'un signal.

------------------------------------------------------------------------

## Anti-pattern 6 --- Persister toutes les projections

Le contexte effectif est souvent éphémère.

Il faut pouvoir reconstruire :

``` text
effective context
```

à partir du canonical state + policy + retrieval state.

------------------------------------------------------------------------

# 40. Hypothèse architecturale centrale pour le projet

L'hypothèse la plus prometteuse issue de la conversation est :

> **Le cœur différenciant d'un futur harness pourrait être moins son
> agent loop que son Context Runtime.**

L'agent loop peut être relativement classique :

``` text
LLM
→ tool
→ result
→ LLM
```

La couche intéressante devient :

``` text
Global State
      ↓
Context Runtime
      ↓
Effective Model View
```

C'est potentiellement là que se joue :

-   la robustesse ;
-   le coût ;
-   la scalabilité ;
-   la qualité des agents ;
-   le partage organisationnel ;
-   la multi-modélisation.

------------------------------------------------------------------------

# 41. Architecture minimale expérimentale recommandée

Une première implémentation pourrait rester très petite :

``` text
SessionStore
      │
      ▼
ContextManager
      │
      ├── HistorySelector
      ├── MemoryProvider
      ├── SkillProvider
      ├── ToolSelector
      └── TokenBudget
      │
      ▼
ModelAdapter
```

Avec une API :

``` typescript
const context = await contextManager.prepare({
  session,
  task,
  model,
  budget,
  policy
})

const response = await model.generate(context)
```

Puis :

``` typescript
await sessionStore.append({
  request,
  response,
  toolCalls,
  stateChanges
})
```

Le point important est que `context` ne soit pas lui-même la source de
vérité.

------------------------------------------------------------------------

# 42. Deuxième étape : introduire MCP

Ajouter :

``` typescript
McpCapabilityProvider
McpResourceProvider
```

Puis :

``` text
ContextManager
    │
    ├── MCP capability discovery
    └── MCP resource retrieval
```

Le runtime peut alors sélectionner :

``` text
tools
resources
```

en fonction de la tâche.

------------------------------------------------------------------------

# 43. Troisième étape : introduire les subagents

Ajouter :

``` typescript
SubagentManager
```

Chaque subagent possède :

``` text
own context
own model
own tools
own budget
own objective
```

et retourne :

``` typescript
AgentResult {
  summary
  findings
  artifacts
  references
  confidence
}
```

Le parent n'a pas besoin de recevoir son transcript complet.

C'est probablement un gain architectural important.

------------------------------------------------------------------------

# 44. Quatrième étape : mémoire

Ajouter :

``` typescript
MemoryStore
MemoryRetriever
MemoryWriter
```

avec des scopes :

``` text
session
project
team
organization
user
```

Le Context Manager décide ce qui est pertinent.

La mémoire ne doit pas automatiquement devenir le prompt.

------------------------------------------------------------------------

# 45. Cinquième étape : configuration organisationnelle

Ajouter :

``` text
PolicyStore
OrgConfig
ProjectConfig
UserConfig
```

avec résolution déterministe.

Puis imposer :

``` text
ContextManager
+
ToolManager
+
McpManager
+
ModelRouter
```

sous contrôle de policy.

------------------------------------------------------------------------

# 46. Pistes d'expérimentation prioritaires

### Expérience A --- Projection simple

Comparer :

``` text
full history
vs
last N messages
vs
projection heuristique
```

Mesurer :

-   coût ;
-   succès ;
-   latence.

------------------------------------------------------------------------

### Expérience B --- RAG pré-appel

Comparer :

``` text
tool-call RAG
vs
pre-model projection RAG
```

Objectif :

-   mesurer si le modèle prend de meilleures décisions ;
-   mesurer le nombre de tool calls ;
-   mesurer le coût total.

------------------------------------------------------------------------

### Expérience C --- MCP capability filtering

Comparer :

``` text
all MCP tools exposed
vs
selected MCP tools
```

Mesurer :

-   tokens ;
-   erreurs de tool selection ;
-   succès.

------------------------------------------------------------------------

### Expérience D --- Subagent isolation

Comparer :

``` text
main agent performs research
vs
research subagent
```

Mesurer :

-   contexte du parent ;
-   coût ;
-   qualité ;
-   latence.

------------------------------------------------------------------------

### Expérience E --- Context Objects

Introduire progressivement :

``` text
Decision
Memory
Artifact
Skill
Resource
Tool
```

et mesurer si la provenance/structure améliore :

-   retrieval ;
-   débogage ;
-   cohérence.

------------------------------------------------------------------------

# 47. Questions de recherche encore ouvertes

1.  Quelle représentation de contexte est la meilleure ?
2.  Faut-il un graphe ou une simple collection d'objets ?
3.  Quand effectuer le retrieval ?
4.  Avant chaque appel ou seulement lors de certains événements ?
5.  Quelle part doit rester contrôlée par le modèle ?
6.  Quelle part doit être contrôlée par le runtime ?
7.  Comment éviter les contradictions entre mémoires ?
8.  Comment mesurer la pertinence réelle ?
9.  Comment allouer un budget de tokens entre sources ?
10. Comment traiter la fraîcheur ?
11. Comment gérer les artefacts volumineux ?
12. Quand déléguer à un subagent ?
13. Comment sélectionner le modèle d'un subagent ?
14. Comment sélectionner les MCP capabilities ?
15. Comment auditer pourquoi une information a été injectée ?
16. Comment gérer plusieurs utilisateurs ?
17. Comment appliquer les policies sans polluer le contexte ?
18. Comment éviter qu'une mémoire incorrecte devienne une vérité
    persistante ?

------------------------------------------------------------------------

# 48. Références d'architecture à surveiller

## OpenCode

Documentation plugins :

https://opencode.ai/v2/docs/build/plugins

Particulièrement :

-   `session.hook("context")`
-   `session.hook("compaction")`
-   model request transformations.

------------------------------------------------------------------------

## Cline

Architecture SDK :

https://github.com/cline/cline/blob/main/sdk/ARCHITECTURE.md

Agents :

https://github.com/cline/cline/blob/main/sdk/packages/agents/README.md

Core :

https://github.com/cline/cline/blob/main/sdk/packages/core/README.md

Le point particulièrement important est la séparation :

``` text
agents = stateless runtime loop
core   = stateful orchestration + context pipeline
```

------------------------------------------------------------------------

## Qwen Code

À surveiller particulièrement pour :

-   memory ;
-   team memory ;
-   auto-memory ;
-   skills ;
-   MCP resources ;
-   subagents ;
-   multi-model.

------------------------------------------------------------------------

## Gemini CLI

À surveiller particulièrement pour :

-   policy engine ;
-   managed/system configuration ;
-   subagents ;
-   skills ;
-   context compression ;
-   MCP.

------------------------------------------------------------------------

# 49. Synthèse finale

Le consensus de la conversation peut être résumé par cette formule :

``` text
                 ┌───────────────────┐
                 │   Canonical State │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Context Runtime   │
                 │                   │
                 │ retrieve          │
                 │ rank              │
                 │ filter            │
                 │ budget            │
                 │ project           │
                 └─────────┬─────────┘
                           │
             ┌─────────────┼──────────────┐
             ▼             ▼              ▼
          Memory          RAG            MCP
             │             │              │
             └─────────────┼──────────────┘
                           │
                           ▼
                    Effective Context
                           │
                           ▼
                       Model Router
                           │
                           ▼
                           LLM
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
              Tools              Subagents
                 │                   │
                 └─────────┬─────────┘
                           ▼
                    Canonical State
```

### Les idées les plus solides

-   Le contexte effectif doit être distinct de l'historique canonique.
-   La compaction et la projection sont deux mécanismes différents.
-   Les subagents sont aussi des mécanismes de partition de contexte.
-   Les skills sont une forme de progressive disclosure / retrieval
    contrôlé.
-   MCP est une couche de capacité et d'accès, pas le Context Manager.
-   Les MCP resources sont particulièrement intéressantes comme sources
    de contexte.
-   Les hooks "just before model call" constituent aujourd'hui un vrai
    point d'ancrage dans des harness OSS actifs.
-   OpenCode et Cline fournissent des seams particulièrement
    exploitables pour expérimenter cette architecture.
-   Qwen est une référence intéressante pour mémoire + skills +
    subagents + MCP.
-   Un environnement partagé nécessite de séparer clairement policy,
    configuration, connaissance, runtime et modèle.

### L'hypothèse de R&D la plus intéressante

> **Construire un Context Runtime explicite, indépendant de l'agent
> loop, qui transforme un état global riche en une vue contextuelle
> minimale, pertinente, traçable et contrainte par budget pour chaque
> appel modèle.**

Cela permettrait de considérer :

``` text
history
memory
RAG
skills
MCP resources
MCP tools
subagent outputs
artifacts
policies
capabilities
```

comme des **sources de contexte/capacités hétérogènes**, plutôt que
comme des mécanismes séparés qui injectent chacun arbitrairement du
texte dans le prompt.

Le projet pourrait ainsi devenir non pas un énième agent loop, mais un
**runtime de projection de contexte et d'orchestration de capacités**,
autour duquel l'agent loop, les modèles, les outils et les interfaces
deviennent des composants interchangeables.

------------------------------------------------------------------------

# 50. Checklist de reprise pour la prochaine itération

## Architecture

-   [ ] Définir explicitement `CanonicalState`.
-   [ ] Définir `EffectiveContext`.
-   [ ] Définir `ContextObject`.
-   [ ] Définir `ContextManager`.
-   [ ] Définir `ContextPolicy`.
-   [ ] Séparer persistence et projection.
-   [ ] Séparer compaction et projection.

## Retrieval

-   [ ] History retrieval.
-   [ ] File/code retrieval.
-   [ ] Memory retrieval.
-   [ ] Skill retrieval.
-   [ ] MCP resource retrieval.
-   [ ] Capability retrieval.

## Agents

-   [ ] Subagent isolation.
-   [ ] Subagent result schema.
-   [ ] Independent model selection.
-   [ ] Context budget par agent.
-   [ ] Parallel execution.

## MCP

-   [ ] Server registry.
-   [ ] Capability discovery.
-   [ ] Tool filtering.
-   [ ] Resource retrieval.
-   [ ] Policy enforcement.
-   [ ] Token-cost accounting.

## Shared environment

-   [ ] Organization config.
-   [ ] Project config.
-   [ ] User config.
-   [ ] Session overrides.
-   [ ] Managed policies.
-   [ ] Shared memory scopes.
-   [ ] Capability allowlist.
-   [ ] Model allowlist.

## Observability

-   [ ] Context provenance.
-   [ ] Token accounting.
-   [ ] Retrieval traces.
-   [ ] Projection traces.
-   [ ] Compaction traces.
-   [ ] Tool/MCP traces.
-   [ ] Subagent traces.

## Évaluation

-   [ ] Task success.
-   [ ] Context size.
-   [ ] Cost.
-   [ ] Latency.
-   [ ] Tool-call count.
-   [ ] Retrieval precision.
-   [ ] Irrelevant-context ratio.
-   [ ] Context provenance correctness.
-   [ ] Memory freshness.
-   [ ] Session recovery.

------------------------------------------------------------------------

# 51. Formule de travail à conserver

Pour les prochaines itérations, garder ce modèle mental :

``` text
Harness
  =
  Agent Loop
  +
  Context Runtime
  +
  Capability Runtime
  +
  Memory
  +
  Policy
  +
  Model Routing
  +
  Persistence
```

et non :

``` text
Harness
  =
  Prompt
  +
  Tools
  +
  Compaction
```

La première formulation laisse beaucoup plus de place à une architecture
évolutive, multi-modèle, multi-agent et multi-utilisateur.

------------------------------------------------------------------------

# 52. Addendum --- deux points depuis l'implémentation existante

*Ajouté 2026-09-26, après relecture contre le code de ce dépôt. Le document
ci-dessus est une base de réflexion issue d'une autre conversation ; ces deux
points ne le contredisent pas, ils nomment ce qui existe déjà ici et ce qui
manque pour pouvoir l'expérimenter.*

## 52.1 La stratégie de contexte est portée par les processors, pas par l'assembleur

Le document parle du `Context Manager` comme s'il contenait la stratégie. Dans
l'implémentation actuelle il n'en contient aucune. Le constat, vérifiable :

``` text
run_suite.arm_monolith   : assemble(objective, ws, token_budget=8000)
m6_arms.run_dloop        : assemble(objective, ws, token_budget=8000)
m7_workflow              : assemble(objective, ws, token_budget=8000)
                           puis  code[:4000]  pour l'étape d'audit
```

`assemble()` est un **mécanisme** : il prend un budget, des `path_hints`
optionnels, une `prior_conclusion` optionnelle, et produit un bundle avec une
trace. Il ne décide de rien. Ce sont les arms qui décident :

- **quel rôle** est instancié, donc quelles instructions arrivent en tête de
  prompt (`roles.ROLE_INSTRUCTIONS`) ;
- **quel budget** ;
- **quels indices de chemin** ;
- **quelle tranche** de l'état est projetée (`code[:4000]`) ;
- **quelle évidence** est réinjectée au tour suivant — `staged` réinjecte
  `"Current state still fails: <labels>"`, `dloop` restaure le meilleur
  snapshot pour que le modèle ne revoie jamais son pire essai, `judge_*`
  réinjecte le verdict du juge.

### Conséquence 1 --- les instructions de processor SONT du contexte

Elles ne sont nommées nulle part comme une source de contexte, et elles sont
pourtant présentes à chaque appel, en première position, avant l'objectif. Le
routage vers un rôle est donc déjà une décision de gestion de contexte. Le
document liste dix sources (§0) ; celle-ci en est une onzième, non nommée.

### Conséquence 2 --- le corpus existant porte déjà une dimension projection

Les arms de M6/M7 couvrent **plusieurs dimensions à la fois**, et certaines sont
explicitement des stratégies d'assemblage de contexte : `judge_fullctx`,
`judge_anchored` et `judge_caveat` diffèrent par ce qui est montré au juge, pas
par la forme de la boucle. Ce n'est pas un étiquetage erroné, c'est une
conception multi-dimensionnelle assumée.

Le point à retenir n'est donc pas "ces arms sont mal nommés" mais : **la
dimension projection est déjà présente dans ~4 000 lignes de résultats, et
l'analyse doit se garder de confondre les dimensions** quand elle les lit. Cette
discipline relève de l'analyse, pas du design des arms.

### Formulation à conserver

> Le Context Manager est **ce qui interprète et exécute** l'assemblage. Il ne
> porte que les stratégies qu'on peut y construire. Aujourd'hui la stratégie
> vit dans les processors ; demain elle pourra être déclarée, mais le
> déplacement doit être explicite, sinon on croira avoir un context manager
> alors qu'on aura un assembleur avec des appelants.

Ce n'est en tension avec aucune décision de conception actuelle. C'est un point
qui gagne à être énoncé plutôt que laissé implicite.

## 52.2 Le graph RAG doit exister comme outil ET comme API de contexte

La base de connaissance prévue ne peut pas n'être exposée que d'une seule
façon, pour une raison expérimentale et non esthétique.

Le document distingue correctement deux familles (§2.1 et §4) :

``` text
tool-call RAG          le modèle décide quand chercher
projection RAG         le runtime décide quoi présenter avant l'appel
```

et l'Expérience B (§46) propose précisément de les comparer. **Cette comparaison
est impossible si la base n'est accessible que par un seul chemin.** Il faut
donc, dès la construction :

``` text
KnowledgeGraph
      │
      ├── surface outil        search_knowledge(query) -> tool_result
      │                        le modèle initie, le coût entre dans le contexte
      │                        de conversation, la décision est observable
      │
      └── surface API contexte kb.select(task, budget, policy) -> ContextObject[]
                               le runtime initie, le coût est un budget alloué,
                               la décision est tracée côté harness
```

Les deux surfaces doivent lire **le même graphe** et produire **la même unité**
(un `ContextObject` avec provenance, §32), sinon la comparaison mesure deux
bases différentes plutôt que deux stratégies d'accès.

Trois mesures deviennent alors possibles sur une même tâche :

| arm | qui décide | ce qu'on mesure |
|---|---|---|
| tool seul | le modèle | nombre d'appels, tokens de résultats, pertinence des requêtes |
| projection seule | le runtime | taille projetée, taux de manque, taux d'inutile |
| les deux | mixte | le runtime pré-charge, le modèle complète |

Le troisième arm est probablement le cas réel, et il n'est mesurable que si les
deux premiers existent séparément.

**Contrainte de construction qui en découle :** ne pas implémenter la
récupération à l'intérieur d'un handler d'outil. L'outil doit être une enveloppe
mince au-dessus de la même fonction que l'API de contexte appelle. Si la logique
vit dans le handler, la surface projection devra la réimplémenter et les deux
divergeront.

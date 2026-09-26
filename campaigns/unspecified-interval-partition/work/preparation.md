# Preparation evidence

Prepared on 2026-09-26 before construction. The fixed corpus has 116 distinct
legal 3-Coloring graphs: 16 hand-labelled edge cases and 100 seeded random
cases, with 74 YES and 42 NO decisions and zero to seven vertices.
`generate_cases.py` retains the generator and seeds; `cases.json` stores
checked outputs. The source oracle enumerates all three-color assignments
and directly validates returned colorings. Exhaustion establishes
NO-SOLUTION for these finite cases. Hand fixtures cover cliques, cycles,
bipartite graphs, an odd wheel and the empty graph.

The target oracle uses Z3 4.16.0 with bounded integer class labels and
closed interval endpoint ranks. It equates every adjacency bit with the
conjunction of different classes and overlapping intervals. Every model
is checked by an independent direct pairwise calculation. UNSAT is
conclusive; unknown is an error. Independent enumeration of all class
assignments and endpoint intervals agreed with Z3 on 36 graph/budget
thresholds for zero to three vertices and budgets zero to two. Hand
fixtures cover a triangle needing three classes, valid shared endpoints,
wrong class labels and illegal budget.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/unspecified-interval-partition/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates seeded graphs,
rechecks source labels and witnesses, then runs independent target
enumeration. The candidate runner uses separate forward and recovery
subprocesses and up to three target representations per source. An
incorrect injected candidate was rejected after target solving and
source validation. No actual reduction candidate exists; the finite
checks do not establish hardness or a general reduction.

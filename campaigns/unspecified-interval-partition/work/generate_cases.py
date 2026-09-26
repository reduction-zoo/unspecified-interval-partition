"""Fix seeded 3-Coloring graphs before reduction construction."""

import json
import random
from pathlib import Path


def graph(n,edges):
    return {"vertices":n,"edges":edges}


def clique(n):
    return [[u,v] for u in range(n) for v in range(u+1,n)]


EDGE_CASES = [
    (graph(0,[]),True), (graph(1,[]),True),
    (graph(2,[]),True), (graph(2,[[0,1]]),True),
    (graph(3,clique(3)),True), (graph(3,[[0,1],[1,2]]),True),
    (graph(4,clique(4)),False),
    (graph(4,[edge for edge in clique(4) if edge != [0,1]]),True),
    (graph(4,[[0,1],[1,2],[2,3],[0,3]]),True),
    (graph(4,[[0,1],[1,2],[2,3]]),True),
    (graph(5,[[0,1],[1,2],[2,3],[3,4],[0,4]]),True),
    (graph(5,clique(5)),False),
    (graph(5,clique(4)),False),
    (graph(5,[[u,v] for u in (0,1) for v in (2,3,4)]),True),
    (graph(6,[[u,v] for u in (0,1,2) for v in (3,4,5)]),True),
    (graph(6,[[0,1],[1,2],[2,3],[3,4],[0,4]]+[[5,v] for v in range(5)]),False),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(4,7)
    if seed % 2 == 0:
        colors = [rng.randrange(3) for _ in range(n)]
        edges = [[u,v] for u in range(n) for v in range(u+1,n)
                 if colors[u] != colors[v] and rng.random() < 0.6]
    else:
        edges = clique(4) + [[u,v] for u in range(4) for v in range(4,n)
                             if rng.random() < 0.35]
        edges += [[u,v] for u in range(4,n) for v in range(u+1,n)
                  if rng.random() < 0.35]
    return graph(n,edges)


def build_cases():
    from check import solve_source
    cases, seen = [], set()

    def add(source,kind,seed=None,hand_answer=None):
        key = json.dumps(source,sort_keys=True,separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and ("coloring" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for source,expected in EDGE_CASES:
        add(source,"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")

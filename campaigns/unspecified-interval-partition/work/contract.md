# Prepared input and output contract

The 3-Coloring source input is `{"vertices": n, "edges": [[u,v], ...]}`
with a simple undirected graph on `0..n-1`. A source output is
`{"coloring": [0,1,2 labels]}` assigning different colors to adjacent
vertices, or `{"status": "NO-SOLUTION"}` exactly when no such coloring
exists. The empty graph has the valid empty coloring.

The target input adds nonnegative integer `"budget": k` to a simple graph.
A target output is `{"classes": [indices], "intervals": [[left,right],
...]}`, one class and one closed interval per vertex. Class indices lie in
`0..k-1`; endpoint weak-order ranks are integers in `0..2n-1` with
`left <= right`. For each pair of vertices, an edge exists exactly when
their classes differ and their intervals intersect, including at a shared
endpoint. Any rational endpoint representation can be compressed to these
weak-order ranks without changing intersections. The alternative
`{"status": "NO-SOLUTION"}` is valid exactly when no representation
exists. An empty graph has the valid empty representation even if `k=0`.

A candidate `algorithm.py` reads source JSON from stdin and writes legal
target JSON to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors, and send
diagnostics to stderr. They must be deterministic and polynomial time, and
recovery must work for every valid target representation.

`check.py --candidate PATH` independently solves constructed targets on the
fixed source corpus and validates each recovered coloring or negative answer.

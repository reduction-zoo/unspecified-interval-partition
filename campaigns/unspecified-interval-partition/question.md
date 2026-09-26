# 3-Coloring → Interval k-graph recognition without a partition

Category: Complexity open

## Source

The source gives a simple graph. Its outputs are proper vertex colorings with at most three colors, or NO-SOLUTION.

## Target

The target gives a graph and k. Find at most k vertex classes and one closed interval per vertex so that adjacency holds exactly for intersecting intervals in different classes, or report NO-SOLUTION. Endpoint weak-order ranks give a finite encoding.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This isolates the difference between recognizing a representation with supplied classes and discovering the classes.

## Difficulty

Both class assignments and interval order are free, so a supplied-partition reduction does not settle the target.

## Literature context

Recognition with a supplied partition does not answer whether a compatible partition and interval representation can be found together.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [arXiv:2503.00672v1](https://arxiv.org/html/2503.00672v1): Müller and Rafiey, arXiv:2503.00672v1, Definition 1, Theorem 2 and Open Problem 3, distinguish polynomial recognition with the partition supplied from the unspecified-partition question. The 2026 proceedings record identifies WG 2025, LNCS 16124, pp. 405–417, DOI 10.1007/978-3-032-11835-6_29. Its deposited accepted file retains the arXiv v1 header and Open Problem 3 on printed p. 5 (PDF p. 6). The final typeset chapter was not independently compared with this deposited file.
- [2026 proceedings record](https://eprints.whiterose.ac.uk/id/eprint/242420/): Müller and Rafiey, arXiv:2503.00672v1, Definition 1, Theorem 2 and Open Problem 3, distinguish polynomial recognition with the partition supplied from the unspecified-partition question. The 2026 proceedings record identifies WG 2025, LNCS 16124, pp. 405–417, DOI 10.1007/978-3-032-11835-6_29. Its deposited accepted file retains the arXiv v1 header and Open Problem 3 on printed p. 5 (PDF p. 6). The final typeset chapter was not independently compared with this deposited file.
- [10.1007/978-3-032-11835-6_29](https://doi.org/10.1007/978-3-032-11835-6_29): Müller and Rafiey, arXiv:2503.00672v1, Definition 1, Theorem 2 and Open Problem 3, distinguish polynomial recognition with the partition supplied from the unspecified-partition question. The 2026 proceedings record identifies WG 2025, LNCS 16124, pp. 405–417, DOI 10.1007/978-3-032-11835-6_29. Its deposited accepted file retains the arXiv v1 header and Open Problem 3 on printed p. 5 (PDF p. 6). The final typeset chapter was not independently compared with this deposited file.
- [deposited accepted file](https://eprints.whiterose.ac.uk/id/eprint/242420/7/Interval%20H-graphs%20.pdf): Müller and Rafiey, arXiv:2503.00672v1, Definition 1, Theorem 2 and Open Problem 3, distinguish polynomial recognition with the partition supplied from the unspecified-partition question. The 2026 proceedings record identifies WG 2025, LNCS 16124, pp. 405–417, DOI 10.1007/978-3-032-11835-6_29. Its deposited accepted file retains the arXiv v1 header and Open Problem 3 on printed p. 5 (PDF p. 6). The final typeset chapter was not independently compared with this deposited file.
- [Interval k-Graphs and Orders](https://arxiv.org/abs/1602.08669): Brown, Flesch and Langley, Interval k-Graphs and Orders, Order 35 (2018), 495–514, studies the cocomparability restriction, not general recognition without a partition. Brown's 2004 doctoral thesis, Variations on Interval Graphs, Theorem 2.9, printed pp. 29–30, proves that interval k-graphs are weakly chordal. The thesis PDF was downloaded and this proof inspected. The primary theorem already excludes every induced cycle of length at least five; the local probe below is not a new graph-theoretic result.
- [Variations on Interval Graphs](https://digital.auraria.edu/downloads/yzr9m-wqp31/AA00005827_00001.pdf): Brown, Flesch and Langley, Interval k-Graphs and Orders, Order 35 (2018), 495–514, studies the cocomparability restriction, not general recognition without a partition. Brown's 2004 doctoral thesis, Variations on Interval Graphs, Theorem 2.9, printed pp. 29–30, proves that interval k-graphs are weakly chordal. The thesis PDF was downloaded and this proof inspected. The primary theorem already excludes every induced cycle of length at least five; the local probe below is not a new graph-theoretic result.

Fixed from board record `website/questions/unspecified-interval-partition.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.

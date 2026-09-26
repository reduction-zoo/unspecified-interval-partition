"""Independent 3-Coloring and interval k-graph oracles."""

import argparse
import json
import subprocess
import sys
from itertools import combinations, product
from pathlib import Path

import z3


def legal_graph(n,edges):
    if type(n) is not int or n < 0 or not isinstance(edges,list):
        return False
    seen = set()
    for edge in edges:
        if (not isinstance(edge,list) or len(edge) != 2
                or any(type(v) is not int or not 0 <= v < n for v in edge)
                or edge[0] == edge[1]):
            return False
        key = tuple(sorted(edge))
        if key in seen:
            return False
        seen.add(key)
    return True


def legal_source(source):
    return isinstance(source,dict) and legal_graph(source.get("vertices"),source.get("edges"))


def legal_target(target):
    return (legal_source(target) and type(target.get("budget")) is int
            and target["budget"] >= 0)


def direct_coloring(source,coloring):
    n = source["vertices"]
    return (isinstance(coloring,list) and len(coloring) == n
            and all(type(c) is int and 0 <= c < 3 for c in coloring)
            and all(coloring[u] != coloring[v] for u,v in source["edges"]))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal 3-Coloring graph")
    for colors in product(range(3),repeat=source["vertices"]):
        if direct_coloring(source,list(colors)):
            return {"coloring":list(colors)}
    return {"status":"NO-SOLUTION"}


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return set(output) == {"coloring"} and direct_coloring(source,output["coloring"])


def direct_representation(target,classes,intervals):
    if not legal_target(target) or not isinstance(classes,list) or not isinstance(intervals,list):
        return False
    n,k = target["vertices"],target["budget"]
    if not (len(classes) == n and len(intervals) == n
            and all(type(c) is int and 0 <= c < k for c in classes)
            and all(isinstance(pair,list) and len(pair) == 2
                    and all(type(p) is int for p in pair)
                    and 0 <= pair[0] <= pair[1] < 2*n for pair in intervals)):
        return False
    edges = {tuple(sorted(edge)) for edge in target["edges"]}
    return all(((classes[u] != classes[v])
                and intervals[u][0] <= intervals[v][1]
                and intervals[v][0] <= intervals[u][1]) == ((u,v) in edges)
               for u in range(n) for v in range(u+1,n))


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal interval k-graph instance")
    n,k = target["vertices"],target["budget"]
    classes = [z3.Int(f"class_{v}") for v in range(n)]
    left = [z3.Int(f"left_{v}") for v in range(n)]
    right = [z3.Int(f"right_{v}") for v in range(n)]
    solver = z3.Solver()
    for v in range(n):
        solver.add(classes[v] >= 0,classes[v] < k)
        solver.add(left[v] >= 0,left[v] <= right[v],right[v] < 2*n)
    edges = {tuple(sorted(edge)) for edge in target["edges"]}
    for u in range(n):
        for v in range(u+1,n):
            adjacency = z3.And(classes[u] != classes[v],left[u] <= right[v],left[v] <= right[u])
            solver.add(adjacency if (u,v) in edges else z3.Not(adjacency))
    outputs = []
    flat = classes+left+right
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive interval solver: {result}")
        model = solver.model()
        cls = [model.eval(x).as_long() for x in classes]
        spans = [[model.eval(left[v]).as_long(),model.eval(right[v]).as_long()] for v in range(n)]
        if not direct_representation(target,cls,spans):
            raise AssertionError("Z3 model violates direct interval representation")
        outputs.append({"classes":cls,"intervals":spans})
        solver.add(z3.Or(*[var != model.eval(var) for var in flat]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return (set(output) == {"classes","intervals"}
            and direct_representation(target,output["classes"],output["intervals"]))


def exhaustive_target(target):
    n,k = target["vertices"],target["budget"]
    choices = [[a,b] for a in range(2*n) for b in range(a,2*n)]
    for classes in product(range(k),repeat=n):
        for intervals in product(choices,repeat=n):
            if direct_representation(target,list(classes),list(intervals)):
                return {"classes":list(classes),"intervals":list(intervals)}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert ("coloring" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        assert ("coloring" in current) == ("coloring" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked = 0
    for n in range(4):
        pairs = list(combinations(range(n),2))
        for mask in range(1 << len(pairs)):
            edges = [list(pair) for i,pair in enumerate(pairs) if mask & (1 << i)]
            for k in range(3):
                target = {"vertices":n,"edges":edges,"budget":k}
                assert ("classes" in solve_target(target)) == ("classes" in exhaustive_target(target))
                checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive interval thresholds")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal interval target: {target}")
        for output in target_solutions(target):
            if not valid_target(target,output):
                raise AssertionError(f"Invalid target oracle output: {output}")
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)

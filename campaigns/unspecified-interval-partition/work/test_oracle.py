from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    triangle = {"vertices":3,"edges":[[0,1],[1,2],[0,2]]}
    assert valid_source(triangle,{"coloring":[0,1,2]})
    assert not valid_source(triangle,{"coloring":[0,0,1]})
    complete_four = {"vertices":4,"edges":[[u,v] for u in range(4) for v in range(u+1,4)]}
    assert solve_source(complete_four) == {"status":"NO-SOLUTION"}
    target = {**triangle,"budget":3}
    assert valid_target(target,{"classes":[0,1,2],"intervals":[[0,1]]*3})
    assert not valid_target({**target,"budget":2},{"classes":[0,1,0],"intervals":[[0,1]]*3})
    assert solve_target({**target,"budget":2}) == {"status":"NO-SOLUTION"}
    assert not legal_target({**target,"budget":-1})


if __name__ == "__main__":
    test_hand_cases()

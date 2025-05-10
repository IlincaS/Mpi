import time
import random
from itertools import combinations
from collections import defaultdict

#resolution algorithm
def resolve(ci, cj):
    resolvents = set()
    for lit in ci:
        if -lit in cj:
            new_clause = (ci.union(cj)) - {lit, -lit}
            resolvents.add(frozenset(new_clause))
    return resolvents

def resolution_algorithm(clauses):
    clauses = set(frozenset(c) for c in clauses)
    new = set()
    while True:
        pairs = combinations(clauses, 2)
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if frozenset() in resolvents:
                return False
            new = new.union(resolvents)
        if new.issubset(clauses):
            return True
        clauses = clauses.union(new)

#DP algorithm
def dp_algorithm(clauses, variables, depth=0, max_depth=50, max_clause_count=500):
    if depth > max_depth or len(clauses) > max_clause_count:
        return False

    if not clauses:
        return True
    if any([not clause for clause in clauses]):
        return False

    var = variables[0] if variables else None
    if var is None:
        return True

    pos_clauses = [c for c in clauses if var in c]
    neg_clauses = [c for c in clauses if -var in c]
    rest_clauses = [c for c in clauses if var not in c and -var not in c]

    new_clauses = []
    for c1 in pos_clauses:
        for c2 in neg_clauses:
            new_clause = list(set(c1 + c2))
            new_clause = [lit for lit in new_clause if lit != var and lit != -var]
            new_clauses.append(new_clause)

    return dp_algorithm(rest_clauses + new_clauses, variables[1:], depth + 1, max_depth, max_clause_count)

#DPLL algorithm
def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = []

    if not clauses:
        return True, assignment
    if any([not clause for clause in clauses]):
        return False, None

    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    while unit_clauses:
        lit = unit_clauses[0]
        assignment = assignment + [lit]
        clauses = [c for c in clauses if lit not in c]
        new_clauses = []
        for c in clauses:
            if -lit in c:
                new_c = [l for l in c if l != -lit]
                if not new_c:
                    return False, None
                new_clauses.append(new_c)
            else:
                new_clauses.append(c)
        clauses = new_clauses
        unit_clauses = [c[0] for c in clauses if len(c) == 1]

    non_empty_clauses = [c for c in clauses if len(c) > 0]
    if not non_empty_clauses:
        return True, assignment

    var = abs(non_empty_clauses[0][0])
    result, a1 = dpll([c[:] for c in clauses] + [[var]], assignment[:])
    if result:
        return True, a1
    return dpll([c[:] for c in clauses] + [[-var]], assignment[:])

#CDCL algorithm
def cdcl(clauses):
    assignment = []
    learned_clauses = []

    def unit_propagate(clauses):
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                if len(clause) == 1:
                    lit = clause[0]
                    if -lit in assignment:
                        return False
                    if lit not in assignment:
                        assignment.append(lit)
                        changed = True
                        for c in clauses:
                            if lit in c:
                                continue
                            if -lit in c:
                                c.remove(-lit)
        return True

    def choose_literal(clauses):
        for clause in clauses:
            for lit in clause:
                if lit not in assignment and -lit not in assignment:
                    return lit
        return None

    while True:
        if not unit_propagate(clauses + learned_clauses):
            if not assignment:
                return False, None
            last = assignment.pop()
            learned_clauses.append([-last])
            continue
        lit = choose_literal(clauses)
        if lit is None:
            return True, assignment
        assignment.append(lit)

#benchmarking algorithm
def generate_3sat_instance(num_vars, num_clauses):
    instance = []
    for _ in range(num_clauses):
        clause = random.sample(range(1, num_vars + 1), 3)
        clause = [lit if random.random() < 0.5 else -lit for lit in clause]
        instance.append(clause)
    return instance

def benchmark_solver(solver_fn, instances, with_vars=False):
    results = []
    for idx, inst in enumerate(instances):
        vars = list(range(1, max(abs(lit) for clause in inst for lit in clause) + 1))
        print(f"\nInstance {idx + 1}:")
        for j, clause in enumerate(inst):
            print(f"Clause {j + 1}: {' ∨ '.join(str(lit) for lit in clause)}")
        start = time.time()
        if with_vars:
            solver_fn(inst, vars)
        else:
            solver_fn(inst)
        end = time.time()
        results.append(end - start)
    return results

#run the example
if __name__ == "__main__":
    instances = [generate_3sat_instance(20, 80) for _ in range(3)]

    print("\nRunning solvers on all instances...\n")

    dpll_times = benchmark_solver(lambda inst: dpll(inst)[0], instances)
    dp_times = benchmark_solver(lambda inst, vars: dp_algorithm(inst, vars), instances, with_vars=True)
    cdcl_times = benchmark_solver(lambda inst: cdcl(inst)[0], instances)

    print("\n=== Solver Timing Summary ===")
    print("DPLL times:", dpll_times)
    print("DP times:", dp_times)
    print("CDCL times:", cdcl_times)

    # Don't uncomment until you want to test Resolution, it may be very slow and it may be crash
    # print("\nBenchmarking Resolution...")
    # res_times = benchmark_solver(resolution_algorithm, instances)
    # print("Resolution times:", res_times)

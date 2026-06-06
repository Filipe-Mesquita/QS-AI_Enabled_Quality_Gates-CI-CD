def manual_gate(coverage, fuzz_failures, mutation_score):

    if coverage < 60:
        return "REJECT"

    if fuzz_failures > 0.2:
        return "REJECT"

    if mutation_score < 0.5:
        return "REJECT"

    return "APPROVE"
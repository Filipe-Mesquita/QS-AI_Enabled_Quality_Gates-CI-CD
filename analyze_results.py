import json

# =====================================================
# Analysis Merges 
# =====================================================
# Analisa os resultados finais do pipeline CI/CD:
#
# - total de merges
# - defeitos que escaparam (defect leakage)
# =====================================================

with open("data/metrics.json") as f:
    data = json.load(f)

# total de merges simulados
total = len(data)

# -----------------------------
# Counters 
# -----------------------------
final_decisions = {}
ai_decisions = {}
human_decisions = {}

leakage = 0
overrides = 0

# -----------------------------
# Agregações de métricas
# -----------------------------
coverage_by_decision = {}
lint_by_decision = {}
complexity_by_decision = {}
fuzz_by_decision = {}
mutation_by_decision = {}

# -----------------------------
# 
# -----------------------------
def inc(dictionary, key):
    if key is None:
        return
    if key not in dictionary:
        dictionary[key] = 0
    dictionary[key] += 1


def add_metric(store, key, value):
    if key not in store:
        store[key] = []
    store[key].append(value)


# -----------------------------
# 
# -----------------------------
for d in data:

    fd = d.get("final_decision")
    ai = d.get("ai_decision")
    human = d.get("human_decision")

    # decisões
    inc(final_decisions, fd)
    inc(ai_decisions, ai)
    inc(human_decisions, human)

    # overrides
    if "OVERRIDE" in str(fd):
        overrides += 1

    # defect leakage
    if fd == "FAIL" and d.get("merge_final_decision") == "GOOD":
        leakage += 1

    # métricas por decisão
    add_metric(coverage_by_decision, fd, d.get("coverage", 0))
    add_metric(lint_by_decision, fd, d.get("lint_errors", 0))
    add_metric(complexity_by_decision, fd, d.get("complexity", 0))
    add_metric(fuzz_by_decision, fd, d.get("fuzz_failures", 0))
    add_metric(mutation_by_decision, fd, d.get("mutation_score", 0))


# -----------------------------
# 
# -----------------------------
def avg(lst):
    return sum(lst) / len(lst) if lst else 0


# -----------------------------
# OUTPUT
# -----------------------------
print("\n============================")
print("PIPELINE ANALYSIS REPORT")
print("============================\n")

print("Total merges:", total)

print("\nFinal decisions:", final_decisions)
print("AI decisions:", ai_decisions)
print("Human decisions:", human_decisions)

print("\nOverrides:", overrides)
print("Defect leakage:", leakage)

print("\n--- METRICS BY DECISION ---")

for decision in final_decisions.keys():
    print("\nDecision:", decision)
    print("  Coverage:", round(avg(coverage_by_decision.get(decision, [])), 3))
    print("  Lint errors:", round(avg(lint_by_decision.get(decision, [])), 3))
    print("  Complexity:", round(avg(complexity_by_decision.get(decision, [])), 3))
    print("  Fuzz failures:", round(avg(fuzz_by_decision.get(decision, [])), 3))
    print("  Mutation score:", round(avg(mutation_by_decision.get(decision, [])), 3))

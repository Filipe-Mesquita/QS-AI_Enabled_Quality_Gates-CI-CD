import json

from quality_gates.ai_gate import AIGate
from quality_gates.manual import ManualGate
from quality_gates.override import apply_override
from quality_gates.metrics_engine import MetricsEngine

from tests.fuzz_tests.fuzz_testing import run_fuzz_tests
from tests.mutation_tests.mutation_testing import run_mutation_tests
from tests.unit_tests import run_unit_tests


# ---------------------------------------------------
# CARREGA MERGES
# ---------------------------------------------------

with open("data/merges.json") as f:
    merges = json.load(f)

ai = AIGate()
manual = ManualGate()
metrics = MetricsEngine()

results = []

# ---------------------------------------------------
# PIPELINE PRINCIPAL
# ---------------------------------------------------

for merge in merges:

    system = merge["system"]

    # ---------------------------
    # 1. UNIT TESTS → COVERAGE
    # ---------------------------
    coverage = run_unit_tests(system)

    # ---------------------------
    # 2. FUZZ TESTS
    # ---------------------------
    fuzz_failures = run_fuzz_tests(system)

    # ---------------------------
    # 3. MUTATION TESTS
    # ---------------------------
    mutation_score = run_mutation_tests(system)

    # ---------------------------
    # 4. AI GATE
    # ---------------------------
    ai_decision, score, confidence = ai.evaluate(
        coverage,
        fuzz_failures,
        mutation_score,
        system
    )

    # ---------------------------
    # 5. HUMAN GATE
    # ---------------------------
    human_decision = manual.review(ai_decision, score)

    # ---------------------------
    # 6. OVERRIDE
    # ---------------------------
    final_decision = apply_override(ai_decision, human_decision, score)

    # ---------------------------
    # 7. METRICS
    # ---------------------------
    metrics.add({
        "system": system,
        "coverage": coverage,
        "fuzz_failures": fuzz_failures,
        "mutation_score": mutation_score,
        "ai_decision": ai_decision,
        "human_decision": human_decision,
        "final_decision": final_decision,
        "merge_final_decision": merge["merge_final_decision"]
    })

metrics.save()


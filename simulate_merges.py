import random
from quality_gates.ai_gate import AIQualityGate
from quality_gates.manual_override import ManualReviewer
from quality_gates.metrics_engine import MetricsEngine


ai_gate = AIQualityGate()
reviewer = ManualReviewer()
metrics = MetricsEngine()


for merge_id in range(1, 101):

    coverage = random.randint(40, 100)
    lint_errors = random.randint(0, 15)
    complexity = random.randint(1, 20)

    ai_result = ai_gate.evaluate(
        coverage,
        lint_errors,
        complexity
    )

    business_critical = random.choice([True, False])

    human_result = reviewer.review(
        ai_result, business_critical)

    defect_leakage = random.choice([0, 1]) if ai_result["decision"] == "PASS" else 0

    """
    metrics.add_result({
        "merge_id": merge_id,
        "coverage": c
    """

import json

from quality_gates.ai_gate import AIGate
from quality_gates.manual import manual_gate
from quality_gates.override import apply_override
from quality_gates.metrics_engine import MetricsEngine
from quality_gates.risk_engine import compute_risk

from tests.fuzz_tests.fuzz_testing import run_fuzz_tests
from tests.mutation_tests.mutation_testing import run_mutation_tests
from tests.unit_tests.unit_testing import run_unit_tests


# ---------------------------------------------------
# Extrair Merges Criados do Ficheiro "merges.json"
# ---------------------------------------------------
# Este ficheiro contém merges gerados pelo ficheiro
# generate_data.py com:
# - system (calculator / passwords / loan)
# - merge_final_decision (GOOD / BAD)
# =====================================================

# Abrir ficheiro e extrair os merges criados para a variável merges
with open("data/merges.json") as f:
    merges = json.load(f)

# Instanciar componentes do Pipelone
ai = AIGate()
metrics = MetricsEngine()

# ---------------------------------------------------
# PIPELINE
# ---------------------------------------------------

# Iterar sobre os merges extraidos
for merge in merges:

    # Extrair o sistema/módulo com o qual o merge atual está relacionado
    system = merge["system"]

    # -----------------------------
    # Tests
    # -----------------------------
    
    # Aplicar testes unitários ao sistema fornecido e obter a coverage
    coverage = run_unit_tests(system)

    # Aplicar fuzz tests e obter os failures para o sistema fornecido
    fuzz_failures = run_fuzz_tests(system)

    # Aplicar mutation tests e obter o score para o sistema fornecido
    mutation_score = run_mutation_tests(system)

    # -----------------------------
    # Risk Engine
    # -----------------------------

    risk_score = compute_risk(coverage, fuzz_failures, mutation_score)

    # -----------------------------
    # AI Gate
    # -----------------------------

    # Simular decisão da IA fornecendo-lhe o risco e o sistema
    # Obtemos a decisão da IA a confiança nessa decisão e o score
    ai_decision, score, confidence = ai.evaluate(risk_score, system)


    # -----------------------------
    # Human Review
    # -----------------------------

    # Simular decisão humana
    human_decision = manual_gate(risk_score)

    # -----------------------------
    # Override
    # -----------------------------

    # Aplicar decisão final em caso de contradição entre a IA e o Humano
    final_decision = apply_override(ai_decision, human_decision)

    # -----------------------------
    # Métricas obtidas
    # -----------------------------
 
    metrics.add({
    "system": system,
    "coverage": coverage,
    "fuzz_failures": fuzz_failures,
    "mutation_score": mutation_score,
    "score": score,
    "confidence": confidence,
    "ai_decision": ai_decision,
    "human_decision": human_decision,
    "final_decision": final_decision,
    "merge_final_decision": merge["merge_final_decision"]
    })

metrics.save()


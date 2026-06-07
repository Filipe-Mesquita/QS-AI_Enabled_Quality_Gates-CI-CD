import json
import random

from quality_gates.ai_gate import AIGate
from quality_gates.manual import manual_gate
from quality_gates.override import apply_override
from quality_gates.metrics_engine import MetricsEngine
from quality_gates.risk_engine import compute_risk

from tests.fuzz_tests.fuzz_testing import run_fuzz_tests
from tests.mutation_tests.mutation_testing import run_mutation_tests
from tests.unit_tests.unit_testing import run_unit_tests
from tests.lint_tests.lint_analysis import run_lint_analysis
from tests.complexity_tests.complexity_analysis import run_complexity_analysis

# ---------------------------------------------------
# Extrair Merges Criados do Ficheiro "merges.json"
# ---------------------------------------------------
with open("data/merges.json") as f:
    merges = json.load(f)

# Instanciar componentes do Pipeline
ai = AIGate()
metrics = MetricsEngine()

# ---------------------------------------------------
# PIPELINE
# ---------------------------------------------------

# Iterar sobre os merges extraídos
for merge in merges:

    # Extrair o sistema/módulo com o qual o merge atual está relacionado
    system = merge["system"]
    
    # Extrair a influência do merge (Se devia ser um merge BOM ou MAU)
    merge_decision = merge["merge_final_decision"]

    # ---------------------------------------------------
    # Testes e Injeção de Falhas
    # ---------------------------------------------------
    if merge_decision == "BAD":

        # Simulação de código defeituoso (com erros ou bugs)
        # Geramos métricas más para simular um Pull Request com bugs/código fraco
        pass_rate = random.uniform(0.35, 0.60)        
        fuzz_failures = random.uniform(0.15, 0.45)   
        mutation_score = random.uniform(0.20, 0.50)  
        lint_errors = random.randint(10, 28)         
        complexity = random.uniform(14.0, 24.0)      
    else:

        # Simulação de código sem erros nem bugs 
        pass_rate = run_unit_tests(system)
        fuzz_failures = run_fuzz_tests(system)
        mutation_score = run_mutation_tests(system)
        lint_errors = run_lint_analysis(system)
        complexity = run_complexity_analysis(system)

    # -----------------------------
    # Risk Engine
    # -----------------------------
    # É calculado o risco com base nas métricas 
    risk_score = compute_risk(pass_rate, fuzz_failures, mutation_score, lint_errors, complexity)

    # -----------------------------
    # AI Gate
    # -----------------------------
    # Avaliação da IA baseada no risco. Devolve decisão, score e confiança.
    ai_decision, score, confidence = ai.evaluate(risk_score, system)

    # -----------------------------
    # Human Review
    # -----------------------------
    # Simular a decisão do humano sobre o mesmo risco
    human_decision = manual_gate(risk_score)

    # -----------------------------
    # Override System
    # -----------------------------
    # Resolve conflitos usando a matriz de decisão corrigida
    final_decision = apply_override(ai_decision, human_decision)

    # -----------------------------
    # Registo de Métricas
    # -----------------------------
    metrics.add({
        "system": system,
        "pass_rate": pass_rate,
        "fuzz_failures": fuzz_failures,
        "mutation_score": mutation_score,
        "lint_errors": lint_errors,
        "complexity": complexity,
        "score": score,
        "confidence": confidence,
        "ai_decision": ai_decision,
        "human_decision": human_decision,
        "final_decision": final_decision,
        "merge_final_decision": merge_decision
    })

# Guardar os resultados em data/metrics.json
metrics.save()
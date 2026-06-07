# ========================================================
# Função compute_risk
# ========================================================
# Calcula o risco associado as métricas obtidas dos testes 
# Este risco "risk" é utilizado pela IA
# ========================================================

def compute_risk(coverage, fuzz_failures, mutation_score):
 
    risk = 0

    # -----------------------------
    # COVERAGE
    # -----------------------------
    if coverage < 60:
        risk += 40
    elif coverage < 80:
        risk += 20

    # -----------------------------
    # FUZZ TESTING
    # -----------------------------
    risk += fuzz_failures * 30

    # -----------------------------
    # MUTATION TESTING
    # -----------------------------
    if mutation_score < 0.5:
        risk += 30
    elif mutation_score < 0.8:
        risk += 10


    if risk > 100:
        risk = 100

    return risk
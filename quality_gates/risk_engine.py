# ========================================================
# Função compute_risk
# ========================================================
# Calcula o risco associado as métricas obtidas dos testes 
# Este risco "risk" é utilizado pela IA
# ========================================================

def compute_risk(pass_rate, fuzz_failures, mutation_score, lint_errors, complexity):
 
    risk = 0

    # -----------------------------
    # Pass Rate 
    # -----------------------------

    # Baixa cobertura indica testes insuficientes
    if pass_rate < 0.60:
        risk += 20
    elif pass_rate < 0.80:
        risk += 10

    # -----------------------------
    # Fuzz Testing 
    # -----------------------------

    # Falhas indicam vulnerabilidade a inputs inesperados
    risk += fuzz_failures * 25

    # -----------------------------
    # Mutation Testing 
    # -----------------------------

    # Mede qualidade real dos testes
    if mutation_score < 0.5:
        risk += 25
    elif mutation_score < 0.8:
        risk += 10

    # -----------------------------
    # Lint Errors
    # -----------------------------    

    # Erros de estilo e possíveis bugs
    risk += lint_errors * 2

    # -----------------------------
    # Complexity
    # -----------------------------

    # Código mais complexo = mais risco de defeitos
    if complexity > 15:
        risk += 15
    elif complexity > 10:
        risk += 8


        
    if risk > 100:
        risk = 100

    return risk
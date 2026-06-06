
# Função que recebe a cobertura dos testes, as falhas no fuzz testing e o score no mutation testing
def compute_risk (coverage,fuzz_failures,mutation_score):

    # Variável que vai conter o risco 
    risk = 0

    # Uma menor cobertura de testes aumenta o risco.
    if coverage < 60:
        risk += 40

    elif coverage < 80:
        risk += 20

    # Falhas encontradas durante fuzz testing.
    risk += fuzz_failures * 10

    # Mutation score baixo aumenta o risco
    if mutation_score < 0.5:
        risk += 30

    elif mutation_score < 0.8:
        risk += 10


    if risk < 30:
        return "LOW"

    elif risk < 60:
        return "MEDIUM"

    else:
        return "HIGH"
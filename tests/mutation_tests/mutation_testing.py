from app.calculator import add
from app.passwords import validate_password


# ---------------------------------------------------
# MUTATION TESTING SIMPLES
# ---------------------------------------------------

def run_mutation_tests():

    killed = 0
    total = 2

    # ---------------- MUTANT 1 ----------------
    def mutant_add(a, b):
        return a + b + 1  # erro artificial

    if mutant_add(2, 3) != add(2, 3):
        killed += 1

    # ---------------- MUTANT 2 ----------------
    def mutant_password(p):
        return True  # ignora regras completamente

    if mutant_password("x") != validate_password("x"):
        killed += 1

    return killed / total
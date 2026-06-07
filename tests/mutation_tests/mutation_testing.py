from app.calculator import add, divide
from app.passwords import validate_password
from app.loan import evaluate_loan


# =====================================================
# Mutation Testing 
# =====================================================
# Mede a capacidade dos testes de detetar erros
# introduzidos no código 
#
# OUTPUT:
#   mutation_score (0 a 1)
# =====================================================

def run_mutation_tests(system):

    killed = 0
    total = 0

    # =========================
    # Calculadora
    # =========================
    if system == "calculator":
        total = 2

        def mutant_add(a, b):
            return a + b + 1

        if mutant_add(2, 3) != add(2, 3):
            killed += 1

        def mutant_divide(a, b):
            if b == 0:
                return 0
            return a / b

        if mutant_divide(10, 2) != divide(10, 2):
            killed += 1


    # =========================
    # Validar Passwords
    # =========================
    elif system == "passwords":
        total = 2

        def mutant_password(p):
            return True

        if mutant_password("x") != validate_password("x"):
            killed += 1

        def mutant_len(p):
            return len(p) > 3

        if mutant_len("1234") != validate_password("1234"):
            killed += 1


    # =========================
    # Aprovar Empréstimos
    # =========================
    elif system == "loan":
        total = 2

        def mutant_loan(income, credit, debt, years, age):
            return "APPROVE"  # ignora risco

        if mutant_loan(1000, 300, 0, 1, 20) != evaluate_loan(1000, 300, 0, 1, 20):
            killed += 1

        def mutant_loan_risk(income, credit, debt, years, age):
            return "REJECT"

        if mutant_loan_risk(8000, 800, 0, 10, 40) != evaluate_loan(8000, 800, 0, 10, 40):
            killed += 1


    return killed / total if total > 0 else 0
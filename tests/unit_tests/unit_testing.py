import random
import string

from app.calculator import add, subtract, multiply, divide
from app.passwords import validate_password
from app.loan import evaluate_loan


# ---------------------------------------------------
# UNIT TESTS
# ---------------------------------------------------
# Simular execução de testes unitários através da 
# geração de inputs.
#
# OUTPUT:
#   pass_rate → valor entre 0 e 100
# =====================================================

def run_unit_tests(system):

    passed = 0
    executed = 0
    total = 20  # número de testes gerados dinamicamente

    # =================================================
    # Calculadora
    # =================================================
    if system == "calculator":

        for _ in range(total):

            a = random.randint(-100, 100)
            b = random.randint(-100, 100)

            executed += 1
            if add(a, b) == a + b:
                passed += 1

            executed += 1
            if subtract(a, b) == a - b:
                passed += 1

            executed += 1
            if multiply(a, b) == a * b:
                passed += 1

            if b != 0:
                executed += 1
                try:
                    if divide(a, b) == a / b:
                        passed += 1
                except:
                    pass

    # =================================================
    # Validar Passwords
    # =================================================

    elif system == "passwords":

        for _ in range(total):

            password = ''.join(
                random.choices(
                    string.ascii_letters +
                    string.digits +
                    string.punctuation,
                    k=random.randint(4, 20)
                )
            )

            executed += 1
            result = validate_password(password)

            has_length = len(password) >= 8
            has_number = any(c.isdigit() for c in password)
            has_symbol = any(c in "!@#$%^&*" for c in password)

            expected = has_length and has_number and has_symbol

            if result == expected:
                passed += 1

    # =================================================
    # Aprovar Empréstimos
    # =================================================
    elif system == "loan":

        for _ in range(total):

            income = random.randint(1000, 8000)
            credit = random.randint(300, 900)
            debt = random.randint(0, 6000)
            years = random.randint(0, 10)
            age = random.randint(18, 80)

            executed += 1
            result = evaluate_loan(income, credit, debt, years, age)

            credit_risk = credit < 600
            debt_risk = debt > (income * 0.5)

            is_risky = credit_risk or debt_risk

            if is_risky:
                expected = "REJECT"
            else:
                expected = "APPROVE"


            if result == expected:
                passed += 1

    # =================================================
    # Pass Rate
    # =================================================
    pass_rate = passed / executed if executed > 0 else 0

    return pass_rate
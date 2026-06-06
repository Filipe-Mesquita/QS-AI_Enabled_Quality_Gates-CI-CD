import random
import string

from app.calculator import add, subtract, multiply, divide
from app.passwords import validate_password
from app.loan import evaluate_loan


# ---------------------------------------------------
# UNIT TESTS DINÂMICOS POR SISTEMA
# ---------------------------------------------------

def run_unit_tests(system):

    passed = 0
    total = 20  # número de testes gerados dinamicamente

    # =================================================
    # CALCULATOR
    # =================================================
    if system == "calculator":

        for _ in range(total):

            a = random.randint(-100, 100)
            b = random.randint(-100, 100)

            # validações dinâmicas (oráculo simples)
            if add(a, b) == a + b:
                passed += 1

            if subtract(a, b) == a - b:
                passed += 1

            if multiply(a, b) == a * b:
                passed += 1

            if b != 0:
                try:
                    if divide(a, b) == a / b:
                        passed += 1
                except:
                    pass

    # =================================================
    # PASSWORDS
    # =================================================
    elif system == "passwords":

        for _ in range(total):

            pwd = ''.join(
                random.choices(
                    string.ascii_letters +
                    string.digits +
                    string.punctuation,
                    k=random.randint(4, 20)
                )
            )

            result = validate_password(pwd)

            # regra simples de referência (heurística)
            expected = (
                len(pwd) >= 8 and
                any(c.isdigit() for c in pwd) and
                any(c in "!@#$%^&*" for c in pwd)
            )

            if result == expected:
                passed += 1

    # =================================================
    # LOAN
    # =================================================
    elif system == "loan":

        for _ in range(total):

            income = random.randint(1000, 8000)
            credit = random.randint(300, 900)
            debt = random.randint(0, 6000)
            years = random.randint(0, 10)
            age = random.randint(18, 80)

            result = evaluate_loan(income, credit, debt, years, age)

            # ORÁCULO SIMPLES (não ground truth real)
            expected = "REJECT" if credit < 600 or debt > income * 0.5 else "APPROVE"

            if result == expected:
                passed += 1

    # =================================================
    # COVERAGE SIMULADA DINÂMICA
    # =================================================
    coverage = passed / (total * 4)

    return coverage
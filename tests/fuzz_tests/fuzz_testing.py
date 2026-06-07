import random
import string

from app.passwords import validate_password
from app.loan import evaluate_loan
from app.calculator import divide


# ---------------------------------------------------
# Fuzz Testing
# ---------------------------------------------------
# Gera inputs aleatórios para encontrar falhas
# inesperadas no sistema.
#
# OUTPUT:
#   fuzz_failures → taxa de falhas (0 a 1)
# =====================================================

def run_fuzz_tests(system):

    failures = 0
    total = 200

    for _ in range(total):

        # =====================
        # Calculadora
        # =====================
        if system == "calculator":
            try:
                divide(
                    random.randint(-1000, 1000),
                    random.randint(-1000, 1000)
                )
            except:
                failures += 1

        # =====================
        # Validar Passwords
        # =====================
        elif system == "passwords":
            try:
                pwd = ''.join(
                    random.choices(
                        string.ascii_letters +
                        string.digits +
                        string.punctuation,
                        k=random.randint(0, 25)
                    )
                )
                validate_password(pwd)
            except:
                failures += 1

        # =====================
        # Aprovar Empréstimos
        # =====================
        elif system == "loan":
            try:
                evaluate_loan(
                    random.randint(1, 8000),
                    random.randint(300, 900),
                    random.randint(0, 6000),
                    random.randint(0, 15),
                    random.randint(18, 90)
                )
            except:
                failures += 1

    return failures / total
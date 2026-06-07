import random
import string

from app.passwords import validate_password
from app.loan import evaluate_loan
from app.calculator import divide

# ---------------------------------------------------
# Fuzz Testing 
# ---------------------------------------------------
def run_fuzz_tests(system):

    failures = 0
    total = 200

    # Lista de inputs errado e extremos comuns 
    corrupt_inputs = [
        None,             # Valor nulo
        "texto_invalido", # Tipo de dados errado (String em vez de Int)
        "",               # String vazia
        -99999999999999,  # Underflow / Número extremamente negativo
        999999999999999,  # Overflow / Número extremamente positivo
        True,             # Booleano disfarçado de número
        [],               # Estruturas de dados inesperadas
    ]

    for _ in range(total):
        
        # Decidir enviar um dado errado (25% de hipótese) ou aleatório normal (75%)
        use_corrupt = random.random() < 0.25

        # =====================
        # Calculadora
        # =====================
        if system == "calculator":
            
            arg1 = random.choice(corrupt_inputs) if use_corrupt else random.randint(-1000, 1000)
            arg2 = random.choice(corrupt_inputs) if use_corrupt else random.randint(-1000, 1000)
            
            try:
                divide(arg1, arg2)
            except Exception:
                failures += 1

        # =====================
        # Validar Passwords
        # =====================
        elif system == "passwords":
            if use_corrupt:

                pwd = random.choice([None, True, 12345, [], {}])
            else:

                pwd = ''.join(random.choices(
                    string.ascii_letters + string.digits + string.punctuation,
                    k=random.randint(0, 50)
                ))
            
            try:
                validate_password(pwd)
            except Exception:
                failures += 1

        # =====================
        # Aprovar Empréstimos
        # =====================
        elif system == "loan":
            if use_corrupt:

                income = random.choice(corrupt_inputs)
                score = random.choice(corrupt_inputs)
                dti = random.choice(corrupt_inputs)
                years = random.choice(corrupt_inputs)
                age = random.choice(corrupt_inputs)
            else:

                income = random.randint(1, 8000)
                score = random.randint(300, 900)
                dti = random.randint(0, 6000)
                years = random.randint(0, 15)
                age = random.randint(18, 90)

            try:
                evaluate_loan(income, score, dti, years, age)
            except Exception:
                failures += 1

    return failures / total
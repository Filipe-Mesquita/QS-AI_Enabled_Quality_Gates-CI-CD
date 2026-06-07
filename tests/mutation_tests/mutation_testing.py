from app.calculator import add, divide
from app.passwords import validate_password


# =====================================================
# Mutation Testing 
# =====================================================
# Mede a capacidade dos testes de detetar erros
# introduzidos no código 
#
# OUTPUT:
#   mutation_score (0 a 1)
# =====================================================

def run_mutation_tests():

    killed = 0
    total = 4


    def mutant_add(a, b):
        return a + b + 1  

    if mutant_add(2, 3) != add(2, 3):
        killed += 1


    def mutant_divide(a, b):
        if b == 0:
            return 0
        return a / b  # ignora erro real (divide-by-zero diferente)

    try:
        if mutant_divide(10, 0) != divide(10, 0):
            killed += 1
    except:
        killed += 1


    def mutant_password(p):
        return True  # ignora todas as regras

    if mutant_password("x") != validate_password("x"):
        killed += 1


    def mutant_password_len(p):
        return len(p) > 3  # ignora regras de segurança

    if mutant_password_len("123") != validate_password("123"):
        killed += 1

    return killed / total
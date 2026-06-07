from app.calculator import add, divide
from app.passwords import validate_password
from app.loan import evaluate_loan

# =====================================================
# TESTES UNITÁRIOS SIMULADOS
# =====================================================
# Estas funções contêm os testes normais do nosso sistema.
# Se a função mutante que passarmos para aqui tiver um erro, o "assert" falha.

def testar_calculadora(funcao_somar, funcao_dividir):
    try:

        assert funcao_somar(2, 3) == 5
        assert funcao_dividir(10, 2) == 5
        return "SOBREVIVEU"  
    except AssertionError:
        return "MORREU"      

def testar_passwords(funcao_validar):
    try:

        assert funcao_validar("12345678aA!") == True
        assert funcao_validar("x") == False
        return "SOBREVIVEU"
    except AssertionError:
        return "MORREU"

def testar_loans(funcao_emprestimo):
    try:

        assert funcao_emprestimo(8000, 800, 0, 10, 40) == "APPROVE"
        assert funcao_emprestimo(1000, 300, 5000, 0, 19) == "REJECT"
        return "SOBREVIVEU"
    except AssertionError:
        return "MORREU"


# =====================================================
# SIMULADOR DE MUTATION TESTING
# =====================================================
def run_mutation_tests(system):
    mutantes_mortos = 0
    total_mutantes = 0

    # -------------------------------------------------
    # CALCULADORA
    # -------------------------------------------------
    if system == "calculator":
        total_mutantes = 2

        # (Soma com bug injetado)
        def mutante_soma_errada(a, b):
            return a + b + 1

        resultado1 = testar_calculadora(mutante_soma_errada, divide)
        if resultado1 == "MORREU":
            mutantes_mortos += 1

        # (Divisão com bug injetado)
        def mutante_divisao_errada(a, b):
            return a / b + 5

        resultado2 = testar_calculadora(add, mutante_divisao_errada)
        if resultado2 == "MORREU":
            mutantes_mortos += 1

    # -------------------------------------------------
    # PASSWORDS
    # -------------------------------------------------
    elif system == "passwords":
        total_mutantes = 2

        # (Aprova sempre tudo, mesmo senhas curtas)
        def mutante_pass_facil(p):
            return True

        resultado1 = testar_passwords(mutante_pass_facil)
        if resultado1 == "MORREU":
            mutantes_mortos += 1

        # (Rejeita sempre tudo)
        def mutante_pass_bloqueada(p):
            return False

        resultado2 = testar_passwords(mutante_pass_bloqueada)
        if resultado2 == "MORREU":
            mutantes_mortos += 1

    # -------------------------------------------------
    # EMPRÉSTIMOS 
    # -------------------------------------------------
    elif system == "loan":
        total_mutantes = 2

        # (Aprova sempre todos os empréstimos)
        def mutante_loan_permissivo(income, credit, debt, years, age):
            return "APPROVE"

        resultado1 = testar_loans(mutante_loan_permissivo)
        if resultado1 == "MORREU":
            mutantes_mortos += 1

        # (Rejeita sempre todos os empréstimos)
        def mutante_loan_rigido(income, credit, debt, years, age):
            return "REJECT"

        resultado2 = testar_loans(mutante_loan_rigido)
        if resultado2 == "MORREU":
            mutantes_mortos += 1

    # Retorna o score final 
    if total_mutantes > 0:
        return mutantes_mortos / total_mutantes
    else:
        return 0
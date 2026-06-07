from app.calculator import add, divide
from app.passwords import validate_password
from app.loan import evaluate_loan

# =====================================================
# 1. TESTES UNITÁRIOS SIMULADOS
# =====================================================
# Estas funções contêm os testes normais do nosso sistema.
# Se a função mutante que passarmos para aqui tiver um erro, o "assert" falha.

def testar_calculadora(funcao_somar, funcao_dividir):
    try:
        # Se a matemática estiver certa, estes asserts passam.
        # Se o mutante alterar o resultado, ocorre um erro (AssertionError).
        assert funcao_somar(2, 3) == 5
        assert funcao_dividir(10, 2) == 5
        return "SOBREVIVEU"  # Se não deu erro, os testes deixaram passar o bug (Mau)
    except AssertionError:
        return "MORREU"      # Se deu erro, os testes apanharam o bug (Bom)

def testar_passwords(funcao_validar):
    try:
        # Uma senha forte deve ser aceite (True)
        assert funcao_validar("12345678aA!") == True
        # Uma senha de apenas uma letra deve ser rejeitada (False)
        assert funcao_validar("x") == False
        return "SOBREVIVEU"
    except AssertionError:
        return "MORREU"

def testar_loans(funcao_emprestimo):
    try:
        # Um perfil excelente deve ser aprovado
        assert funcao_emprestimo(8000, 800, 0, 10, 40) == "APPROVE"
        # Um perfil muito mau deve ser rejeitado
        assert funcao_emprestimo(1000, 300, 5000, 0, 19) == "REJECT"
        return "SOBREVIVEU"
    except AssertionError:
        return "MORREU"


# =====================================================
# 2. SIMULADOR DE MUTATION TESTING
# =====================================================
def run_mutation_tests(system):
    mutantes_mortos = 0
    total_mutantes = 0

    # -------------------------------------------------
    # CASO 1: CALCULADORA
    # -------------------------------------------------
    if system == "calculator":
        total_mutantes = 2

        # Criamos o Mutante 1 (Soma com bug injetado)
        def mutante_soma_errada(a, b):
            return a + b + 1

        # Corremos os testes da calculadora usando este mutante
        resultado1 = testar_calculadora(mutante_soma_errada, divide)
        if resultado1 == "MORREU":
            mutantes_mortos += 1

        # Criamos o Mutante 2 (Divisão com bug injetado)
        def mutante_divisao_errada(a, b):
            return a / b + 5

        resultado2 = testar_calculadora(add, mutante_divisao_errada)
        if resultado2 == "MORREU":
            mutantes_mortos += 1

    # -------------------------------------------------
    # CASO 2: PASSWORDS
    # -------------------------------------------------
    elif system == "passwords":
        total_mutantes = 2

        # Criamos o Mutante 1 (Aprova sempre tudo, mesmo senhas curtas)
        def mutante_pass_facil(p):
            return True

        resultado1 = testar_passwords(mutante_pass_facil)
        if resultado1 == "MORREU":
            mutantes_mortos += 1

        # Criamos o Mutante 2 (Rejeita sempre tudo)
        def mutante_pass_bloqueada(p):
            return False

        resultado2 = testar_passwords(mutante_pass_bloqueada)
        if resultado2 == "MORREU":
            mutantes_mortos += 1

    # -------------------------------------------------
    # CASO 3: EMPRÉSTIMOS (LOAN)
    # -------------------------------------------------
    elif system == "loan":
        total_mutantes = 2

        # Criamos o Mutante 1 (Aprova sempre todos os empréstimos)
        def mutante_loan_permissivo(income, credit, debt, years, age):
            return "APPROVE"

        resultado1 = testar_loans(mutante_loan_permissivo)
        if resultado1 == "MORREU":
            mutantes_mortos += 1

        # Criamos o Mutante 2 (Rejeita sempre todos os empréstimos)
        def mutante_loan_rigido(income, credit, debt, years, age):
            return "REJECT"

        resultado2 = testar_loans(mutante_loan_rigido)
        if resultado2 == "MORREU":
            mutantes_mortos += 1

    # Retorna o score final (percentagem de mutantes apanhados)
    if total_mutantes > 0:
        return mutantes_mortos / total_mutantes
    else:
        return 0
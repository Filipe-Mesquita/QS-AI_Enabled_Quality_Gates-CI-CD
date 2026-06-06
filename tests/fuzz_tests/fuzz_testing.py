import random
from app.passwords import validate_password
from app.loan import evaluate_loan
from app.calculator import divide


# Função responsável por gerar testes aleatórios (fuzz testing)
# O objetivo é fornecer muitos dados aleatórios para verificar se ocorrem erros inesperados
# Devolve a taxa de falhas encontrada durante os testes
def run_fuzz():

    # Variável que vai conter o nº de falhas encontradas
    failures = 0
    # Nº total de testes a executar
    total = 300

    for _ in range(total):

        # Teste calculadora 
        try:
            # Gera valores aleatórios para testar a função dividir
            divide(random.randint(-1000,1000), random.randint(-1000,1000))
        except:
            failures += 1

        # Teste passwords
        try:
            # Gera uma password aleatória entre 0 e 20
            # Seleciona caracteres aleatórios da lista indicada
            # Junta todos os caracteres selecionados numa única string
            validate_password(''.join(random.choices("abc123!@", k=random.randint(0,20))))
        except:
            failures += 1

        # Teste empréstimos
        try:
            # Gera valores aleatórios para simular diferentes clientes a solicitar empréstimo
            evaluate_loan(
                random.randint(1, 5000),
                random.randint(300, 900),
                random.randint(0, 5000),
                random.randint(0, 10),
                random.randint(18, 80)
            )
        except:
            failures += 1

    # Devolve a taxa de falhas
    return failures / total
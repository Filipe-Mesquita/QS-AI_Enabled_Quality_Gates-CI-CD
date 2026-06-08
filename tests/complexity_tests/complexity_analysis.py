import json
import subprocess


# =====================================================
# COMPLEXITY ANALYSIS
# =====================================================
# Executa Radon para obter a complexidade do sistema.
#
# OUTPUT:
#   complexity
# =====================================================

def run_complexity_analysis(system):

    # Path do ficheiro a analisar
    file_path = f"app/{system}.py"

    # Executa o comando no terminal "radon cc app/loan.py -j", para obter a complexidade
    # Devolve o resultado em JSON
    result = subprocess.run(
        [
            "radon",
            "cc",
            file_path,
            "-j"
        ],
        capture_output=True,
        text=True
    )

    # Se não existir output, então devolver 0
    # O mais provável é o ficheiro estar vazio
    if not result.stdout:
        return 0


    data = json.loads(result.stdout)

    functions = data[file_path]

    if len(functions) == 0:
        return 0

    total_complexity = 0

    # Percorrer todas as funções detetadas pelo Radon e adicionar o valor correspondente a complexidade
    for function in functions:
        total_complexity += function["complexity"]  

    # Calcular a complexidade média
    average_complexity = total_complexity / len(functions)

    # Arredondar o resultado com duas casas decimais
    return round(average_complexity, 2)
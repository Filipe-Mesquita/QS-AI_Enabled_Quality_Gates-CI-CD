import subprocess


# =====================================================
# LINT ANALYSIS
# =====================================================
# Executa flake8 sobre o sistema e conta
# quantos erros foram encontrados.
#
# OUTPUT:
#   lint_errors
# =====================================================

def run_lint_analysis(system):

    # Path do ficheiro a analisar
    file_path = f"app/{system}.py"

    # Executa no terminal o comando flake8 app/system
    # O flake8, imprime uma linha por cada erro encontrado
    result = subprocess.run(
        ["flake8", file_path],
        capture_output=True,
        text=True
    )

    # Se o resultado estiver vazio então não foi encontrado nenhum erro
    if not result.stdout:
        return 0

    # Dividir a string obtida numa lista com as linhas, e devolver o tamanho da lista
    lint_errors = len(result.stdout.splitlines())

    return lint_errors
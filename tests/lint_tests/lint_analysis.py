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

    file_path = f"app/{system}.py"

    result = subprocess.run(
        ["flake8", file_path],
        capture_output=True,
        text=True
    )

    if not result.stdout:
        return 0

    lint_errors = len(result.stdout.splitlines())

    return lint_errors
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

    file_path = f"app/{system}.py"

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

    if not result.stdout:
        return 0

    data = json.loads(result.stdout)

    functions = data[file_path]

    if len(functions) == 0:
        return 0

    total_complexity = 0

    for function in functions:
        total_complexity += function["complexity"]

    average_complexity = total_complexity / len(functions)

    return round(average_complexity, 2)
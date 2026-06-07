import json

# =====================================================
# ANALYSIS MODULE
# =====================================================
# Analisa os resultados finais do pipeline CI/CD:
#
# - total de merges
# - defeitos que escaparam (defect leakage)
# =====================================================

with open("data/metrics.json") as f:
    data = json.load(f)

# total de merges simulados
total = len(data)

# calcula defect leakage com segurança
leakage = 0

for d in data:

    if d.get("final_decision") == "FAIL":

        if d.get("merge_final_decision") == "GOOD":
            leakage += 1

print("Total merges:", total)
print("Defect Leakage:", leakage)
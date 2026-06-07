import json

# =====================================================
# Analysis Merges 
# =====================================================
# Analisa os resultados finais do pipeline CI/CD:
# - total de merges
# - frequências de overrides detalhadas 
# - defeitos que escaparam (defect leakage) 
# =====================================================

with open("data/metrics.json") as f:
    data = json.load(f)

# total de merges simulados
total = len(data)

# -----------------------------
# Counters 
# -----------------------------
final_decisions = {}
ai_decisions = {}
human_decisions = {}

leakage = 0
overrides = 0

# -----------------------------
# Agregações de métricas
# -----------------------------
pass_rate_by_decision = {}
lint_by_decision = {}
complexity_by_decision = {}
fuzz_by_decision = {}
mutation_by_decision = {}

# -----------------------------
# Funções auxiliares
# -----------------------------
def inc(dictionary, key):
    if key is None:
        return
    if key not in dictionary:
        dictionary[key] = 0
    dictionary[key] += 1


def add_metric(store, key, value):
    if key not in store:
        store[key] = []
    store[key].append(value)


# -----------------------------
# Processamento de Dados
# -----------------------------
for d in data:

    fd = d.get("final_decision")
    ai = d.get("ai_decision")
    human = d.get("human_decision")
    ground_truth = d.get("merge_final_decision")

    # Contagem de decisões
    inc(final_decisions, fd)
    inc(ai_decisions, ai)
    inc(human_decisions, human)

    # ---------------------------------------------------
    # Deteção de Overrides 
    # ---------------------------------------------------
    
    if ai != fd and fd not in ["OVERRIDE_APPROVE", "OVERRIDE_REJECT"]:
        # Captura os casos onde herdou "APPROVE" ou "REJECT" diretamente do humano divergindo da IA
        overrides += 1
    
    elif "OVERRIDE" in str(fd):
        # Captura os casos explícitos de alteração de estado extremo
        overrides += 1

    # ---------------------------------------------------
    # Deteção de Defect Leakage (RQ1)
    # ---------------------------------------------------
    # O pipeline permitiu o merge (APPROVE ou OVERRIDE_APPROVE), mas o código era instável (BAD)
    if fd in ["APPROVE", "OVERRIDE_APPROVE"] and ground_truth == "BAD":
        leakage += 1

    # Agregação de métricas por decisão final
    add_metric(pass_rate_by_decision, fd, d.get("pass rate", 0))
    add_metric(lint_by_decision, fd, d.get("lint_errors", 0))
    add_metric(complexity_by_decision, fd, d.get("complexity", 0))
    add_metric(fuzz_by_decision, fd, d.get("fuzz_failures", 0))
    add_metric(mutation_by_decision, fd, d.get("mutation_score", 0))


def avg(lst):
    return sum(lst) / len(lst) if lst else 0


# -----------------------------
# OUTPUT 
# -----------------------------
print("\n============================")
print("PIPELINE ANALYSIS REPORT")
print("============================\n")

print(f"Total merges analisados: {total}")

print("\n--- DISTRIBUIÇÃO DE DECISÕES ---")
print(f"Decisões da IA: {ai_decisions}")
print(f"Decisões Humanas: {human_decisions}")
print(f"Decisões Finais do Pipeline: {final_decisions}")

print("\n--- MÉTRICAS DE CONFIANÇA E ACERTO ---")
print(f"Frequência de Overrides Humanos (RQ2): {overrides} ({round((overrides/total)*100, 1)}%)")
print(f"Taxa de Defect Leakage (RQ1): {leakage} casos detetados")

print("\n--- COMPORTAMENTO DAS MÉTRICAS POR DECISÃO FINAL ---")

for decision in final_decisions.keys():
    print(f"\n[Decisão: {decision}]")
    print(f"  > Média Pass Rate:       {round(avg(pass_rate_by_decision.get(decision, [])), 3)}")
    print(f"  > Média Erros Lint:     {round(avg(lint_by_decision.get(decision, [])), 3)}")
    print(f"  > Média Complexidade:   {round(avg(complexity_by_decision.get(decision, [])), 3)}")
    print(f"  > Média Falhas Fuzz:    {round(avg(fuzz_by_decision.get(decision, [])), 3)}")
    print(f"  > Média Mutation Score: {round(avg(mutation_by_decision.get(decision, [])), 3)}")
print("\n============================")
import pandas as pd

# =====================================================
# Classe Metrics Engine
# =====================================================
# Responsável por armazenar todos os resultados do
# pipeline CI/CD simulado.
#
# =====================================================

class MetricsEngine:

    def __init__(self):
        self.data = []

    # Função para registar/guardar um merge
    def add(self, row):

        self.data.append(row)

    # Função para guardar todos os dados num ficheiro JSON (metrics.json)
    def save(self, path="data/metrics.json"):
        
        df = pd.DataFrame(self.data)
        df.to_json(path, orient="records", indent=2)
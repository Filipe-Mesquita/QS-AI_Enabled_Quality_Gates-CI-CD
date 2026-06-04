import json
import pandas as pd


class MetricsEngine:

    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def save_json(self, filename="data/pipeline_results.json"):
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=4)

    def save_csv(self, filename="data/metrics.csv"):
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)

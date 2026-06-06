import pandas as pd

class MetricsEngine:

    def __init__(self):
        self.data = []

    def add(self, row):
        self.data.append(row)

    def save(self, path):
        pd.DataFrame(self.data).to_json(path, orient="records")
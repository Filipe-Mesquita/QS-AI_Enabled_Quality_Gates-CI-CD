import json

data = json.load(open("data/metrics.json"))

print("Total:", len(data))
print("Leakage:", sum(d["leakage"] for d in data))
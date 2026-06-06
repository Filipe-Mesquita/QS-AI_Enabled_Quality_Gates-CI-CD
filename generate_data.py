import random
import json

SYSTEMS = ["calculator", "passwords", "loan"]


# Função para gerar merges 
def generate_merges(n=100):

    data = []

    for i in range(n):
        merge = {
            "merge_id": i,
            "system": random.choice(SYSTEMS),
            "merge_final_decision": random.choice(["GOOD", "BAD"])
        }
        
        data.append(merge)

    with open("data/merges.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"{n} merges gerados com sucesso.")


if __name__ == "__main__":
    generate_merges()
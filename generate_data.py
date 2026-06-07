import random
import json

# Diferentes módulos/sistemas a ser avaliados
# Presentes na diretoria app (calculadora, validar passwords, aprovar empréstimos)
SYSTEMS = ["calculator","passwords","loan"]

# Função para criar merges
def generate_merges(n=100):

    # Variável que vai conter os merges criados
    merges = []

    for merge_id in range(n):

        # Cada merge criado vai conter:
        # merge_id -> corresponde ao id do merge criado
        # system -> Sistema/Módulo utilizado no merge (Calculadora,Passwords ou Empréstimos)
        # merge_final_decision -> Variável que representa o significado após o merge (Diz se o merge foi bom ou mau para o sistema)
        merges.append({

            "merge_id": merge_id,

            "system": random.choice(SYSTEMS),

            "merge_final_decision": random.choice(["GOOD","BAD"])
        })

    # Gravar os merges criados no ficheiro merges.json
    with open("data/merges.json", "w") as f:
        json.dump(merges, f, indent=4)
    

if __name__ == "__main__":
    # Chamar a função para gerar os merges
    generate_merges()
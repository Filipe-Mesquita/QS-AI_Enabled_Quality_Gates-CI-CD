import re
from pathlib import Path


# =====================================================
# Extrair Passwords Conhecidas/Fracas
# =====================================================

file_passwords = Path("data/1000-most-common-passwords.txt")

# Variável que vai conter as passwords
weak_passwords = set()

# Se o path para o ficheiro existir
if file_passwords.exists():

    # Abrir ficheiro
    with open(file_passwords, "r", encoding="utf-8") as file:

        for line in file:

            password = line.strip().lower()

            # Adicionar passwords ao set
            if password:
                weak_passwords.add(password)


# =====================================================
# Função para validar a segurança de uma password
# =====================================================
#   A password recebe pontos se cumprir determinados requisitos
#
# =====================================================

def validate_password(password):

    # Variável que vai conter o score da password
    score = 0

    # Verfica se a password possui mais de 8 caracteres
    if len(password) >= 8:
        score += 1

    # Verfica se a password possui mais de 12 caracteres
    # Maior password, maior a dificuldade em ser descoberta
    if len(password) >= 12:
        score += 1

    # Verifica se a password contém letras maiúsculas
    if re.search(r"[A-Z]", password):
        score += 1

    # Verifica se a password contém letras minúsculas
    if re.search(r"[a-z]", password):
        score += 1

    # Verifica se a password contém números
    if re.search(r"\d", password):
        score += 1

    # Verifica se a password contém caracteres especiais
    if re.search(r"[!@#$%^&*]", password):
        score += 1

    # Se a password avaliada for uma das presentes no ficheiro
    # Reduzir a pontuação da mesma
    if password.lower() in weak_passwords:
        score -= 3

    # Password válida se atingir uma pontuação maior ou igual a 5
    return score >= 5
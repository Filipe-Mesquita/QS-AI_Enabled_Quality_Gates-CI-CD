import re

# Função para validar a segurança de uma determinada password
# A password recebe pontos se cumprir determinados requisitos
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

    # Lista com passwords conhecidas/muito utilizadas
    # Ir buscara a lista de mais utilizadas !!
    weak_passwords = ["1234", "password"]

    # Se a password recebida for uma das presentes na lista
    # Reduzir a pontuação da mesma
    for weak_password in weak_passwords:

        if weak_password in password.lower():
            score -= 2
            break

    # Password válida se atingir uma pontuação maior ou igual a 5
    return score >= 5
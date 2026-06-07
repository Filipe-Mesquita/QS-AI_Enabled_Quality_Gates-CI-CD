# =====================================================
# Função para Validar um Empréstimo
# =====================================================
# Simular um sistema de avaliação de risco para
# aprovação de empréstimos.
#
# =====================================================


def evaluate_loan(income, credit_score, debt, employment_years, age) :

    # Variável que vai conter o risco associado ao empréstimo
    risk = 0

    # --------------------------------------------
    # Pontuação de Crédito
    # --------------------------------------------
    if credit_score >= 750:
        pass

    elif credit_score >= 650:
        risk += 20

    else:
        risk += 40

    # --------------------------------------------
    # Relação entre a Dívida e o Rendimento
    # --------------------------------------------
    
    # Variável que vai conter a relação entre a dívida e o rendimento.
    if income > 0:
        dti = debt / income
    else:
        dti = 1


    if dti < 0.2:
        pass

    elif dti < 0.4:
        risk += 20

    else:
        risk += 40

    # --------------------------------------------
    # Histórico Empregado
    # --------------------------------------------
    if employment_years >= 5:
        pass

    elif employment_years >= 2:
        risk += 15

    else:
        risk += 30

    # --------------------------------------------
    # Idade
    # --------------------------------------------
    if 25 <= age <= 55:
        pass

    elif age < 25:
        risk += 15

    else:
        risk += 10


    # --------------------------------------------
    # Decião Final
    # --------------------------------------------
    if risk <= 30:
        return "APPROVE"

    elif risk <= 60:
        return "REVIEW"

    return "REJECT"

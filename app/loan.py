
# Função que simula um sistema de aprovação de empréstimos
def evaluate_loan(income, credit_score, debt, employment_years, age):

    #  Variável que vai conter o risk de fazer o empréstimo
    risk = 0


    if credit_score >= 750:
        risk += 0
    
    elif credit_score >= 650:
        risk += 20
    
    else:
        risk += 40

    # Variável que vai conter a relação entre a dívida e o income.
    if income > 0:
        dti = debt / income
    else:
        dti = 1


    if dti < 0.2:
        risk += 0

    elif dti < 0.4:
        risk += 20
    
    else:
        risk += 40


    if employment_years >= 5:
        risk += 0
    
    elif employment_years >= 2:
        risk += 15
    
    else:
        risk += 30

    
    if 25 <= age <= 55:
        risk += 0
    
    elif age < 25:
        risk += 15
    
    else:
        risk += 10

    
    if risk <= 30:
        return "APPROVE"
    
    elif risk <= 60:
        return "REVIEW"
    
    else:
        return "REJECT"
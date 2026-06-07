# =====================================================
# CALCULADORA
# =====================================================

# Função soma de dois valores fornecidos
def add(a, b):

    return a + b

# Função subtração entre dois valores fornecidos
def subtract(a, b):

    return a - b


# Função multiplicação entre dois valores fornecidos
def multiply(a, b):

    return a * b

# Função dividir entre dois valores fornecidos
# Lança uma exceção caso o divisor seja zero
def divide(a, b):

    if b == 0:
        raise ValueError("Division by zero")

    return a / b
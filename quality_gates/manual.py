# =====================================================
# Função Manual Gate (HUMAN-IN-THE-LOOP)
# =====================================================
# Simula decisão de um Humano.
#
# =====================================================

def manual_gate(risk_score):
    
    if risk_score > 70:
        return "REJECT"

    if risk_score > 40:
        return "REVIEW"

    return "APPROVE"
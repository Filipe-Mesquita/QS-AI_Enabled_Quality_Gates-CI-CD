# =====================================================
# Função Manual Gate (HUMAN-IN-THE-LOOP)
# =====================================================
# Simula decisão de um Humano.
#
# =====================================================

def manual_gate(risk_score):
    
    # 75
    if risk_score > 95:
        return "REJECT"

    # 40
    if risk_score > 75:
        return "REVIEW"

    return "APPROVE"
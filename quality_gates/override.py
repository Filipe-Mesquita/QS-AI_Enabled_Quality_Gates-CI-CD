# =====================================================
# Função Override 
# =====================================================
# Decisão final combinando IA + humano
#
# =====================================================

def apply_override(ai_decision, manual_decision):

    # IA falha mas Humano corrige
    if ai_decision == "FAIL" and manual_decision == "APPROVE":
        return "OVERRIDE_APPROVE"

    # IA aprova mas Humano rejeita
    if ai_decision == "APPROVE" and manual_decision == "REJECT":
        return "OVERRIDE_REJECT"

    # Em caso de REVIEW manter decisão do Humano
    if ai_decision == "REVIEW":
        return manual_decision
    
    # Humano está em dúvida (REVIEW), mas a IA tem a certeza (APPROVE ou REJECT)
    if manual_decision == "REVIEW":
        return ai_decision

    return ai_decision
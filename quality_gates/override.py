# =====================================================
# Função Override 
# =====================================================
# Decisão final combinando IA + humano
#
# =====================================================


# teste teste teste
def apply_override(ai_decision, manual_decision):

    # IA rejeita mas Humano assume o risco e aprova
    if ai_decision == "REJECT" and manual_decision == "APPROVE":
        return "OVERRIDE_APPROVE"

    # IA aprova mas Humano deteta algo e rejeita
    if ai_decision == "APPROVE" and manual_decision == "REJECT":
        return "OVERRIDE_REJECT"

    # IA está em dúvida (REVIEW) mas o Humano toma uma ação direta
    if ai_decision == "REVIEW" and manual_decision == "APPROVE":
        return "OVERRIDE_APPROVE"
    
    if ai_decision == "REVIEW" and manual_decision == "REJECT":
        return "OVERRIDE_REJECT"
    
    # Humano está em dúvida (REVIEW), mas a IA tem a certeza (APPROVE ou REJECT)
    if manual_decision == "REVIEW":
        return ai_decision

    
    return ai_decision
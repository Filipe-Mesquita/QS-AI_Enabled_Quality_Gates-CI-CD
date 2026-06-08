# =====================================================
# AI Quality Gate
# =====================================================
# Este módulo simula uma decisão automática baseada no 
# risco calculado a partir dos resultados dos testes.
#
# =====================================================

class AIGate:

    def evaluate(self, risk_score, system):
        
        score = 100 - risk_score

        # 70
        if score >= 30:
            decision = "APPROVE"
        # 50
        elif score >= 15:          
            decision = "REVIEW"
        else:                      
            decision = "REJECT"


        if decision == "REVIEW":
            confidence = abs(score - 60.0) / 10.0
        elif decision == "APPROVE":
            confidence = (score - 70) / 30
        else:
            confidence = (50 - score) / 50

        # Garantir limites válidos [0.0, 1.0]
        confidence = max(0.0, min(1.0, round(confidence, 2)))


        return decision, score, confidence
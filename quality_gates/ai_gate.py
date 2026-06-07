# =====================================================
# AI Quality Gate
# =====================================================
# Este módulo simula uma decisão automática baseada no 
# risco calculado a partir dos resultados dos testes.
#
#   Elementos obtidos a partir dos testes:
# - Coverage (qualidade dos testes unitários)
# - Fuzz Failures (robustez)
# - Mutation Score (qualidade dos testes)
# =====================================================


class AIGate:

    def evaluate(self, risk_score, system):

        score = 100 - risk_score

        # Decisão
        if score >= 70:
            decision = "APPROVE"

        elif score >= 50:
            decision = "REVIEW"

        else:
            decision = "FAIL"



        if decision == "REVIEW":
            confidence = abs(score - 57.5) / 12.5
        
        elif decision == "APPROVE":
            confidence = (score - 70) / 30
        
        else:
            confidence = (45 - score) / 45

        # Garantir que a confiança fica entre 0.0 e 1.0
        confidence = max(0.0, min(1.0, round(confidence, 2)))


        return decision, score, confidence
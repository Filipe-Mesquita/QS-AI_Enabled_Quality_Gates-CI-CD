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
            decision = "PASS"

        elif score >= 50:
            decision = "REVIEW"

        else:
            decision = "FAIL"

        # Confiança
        confidence = abs(score - 70) / 30
        confidence = min(1.0, confidence)

        return decision, score, confidence
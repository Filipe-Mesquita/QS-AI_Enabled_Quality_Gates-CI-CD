import random


class AIQualityGate:

    def evaluate(self, coverage, lint_errors, complexity):

        score = 100

        score -= max(0, 80 - coverage)
        score -= lint_errors * 2
        score -= complexity

        uncertainty = random.randint(-10, 10)
        score += uncertainty

        if score >= 70:
            return {
                "decision": "PASS",
                "score": score,
                "confidence": "HIGH"
            }

        elif score >= 50:
            return {
                "decision": "WARNING",
                "score": score,
                "confidence": "MEDIUM"
            }

        return {
            "decision": "FAIL",
            "score": score,
            "confidence": "LOW"
        }

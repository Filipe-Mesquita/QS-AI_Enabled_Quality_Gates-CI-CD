class AIQualityGate:

    def evaluate(self, coverage, fuzz_failures, mutation_score, step):

        score = 100

        if coverage < 60:
            score -= 30
        elif coverage < 80:
            score -= 15

        score -= fuzz_failures * 15

        if mutation_score < 0.5:
            score -= 30
        elif mutation_score < 0.8:
            score -= 10

        score -= (step / 200) * 15

        if score >= 70:
            decision = "PASS"
        elif score >= 50:
            decision = "REVIEW"
        else:
            decision = "FAIL"

        confidence = min(1.0, abs(score - 70) / 30)

        if confidence < 0.35:
            decision = "REVIEW"

        return decision, score, confidence
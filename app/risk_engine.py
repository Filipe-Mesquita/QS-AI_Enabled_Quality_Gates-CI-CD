class RiskEngine:

    @staticmethod
    def calculate_risk(test_coverage, lint_errors, complexity):

        risk = 0

        if test_coverage < 80:
            risk += 40

        if lint_errors > 5:
            risk += 30

        if complexity > 10:
            risk += 30

        return min(risk, 100)
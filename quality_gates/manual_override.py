class ManualReviewer:

    def review(self, ai_decision, business_critical=False):

        if ai_decision["decision"] == "FAIL":

            if business_critical:
                return "OVERRIDE_APPROVED"

            return "REJECTED"

        return "APPROVED"

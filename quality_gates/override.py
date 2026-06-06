def apply_override(ai_decision, manual_decision):

    if ai_decision == "FAIL" and manual_decision == "APPROVE":
        return "OVERRIDE_APPROVE"

    if ai_decision == "PASS" and manual_decision == "REJECT":
        return "OVERRIDE_REJECT"

    return ai_decision
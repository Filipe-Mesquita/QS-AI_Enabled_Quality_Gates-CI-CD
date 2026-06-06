from app.loan import evaluate_loan

def test_approve():
    assert evaluate_loan(5000, 780, 200, 6, 40) == "APPROVE"

def test_reject():
    assert evaluate_loan(2000, 500, 1500, 1, 22) == "REJECT"
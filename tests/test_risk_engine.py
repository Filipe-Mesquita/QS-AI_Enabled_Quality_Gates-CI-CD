from app.risk_engine import RiskEngine


def test_low_risk():
    risk = RiskEngine.calculate_risk(90, 1, 2)
    assert risk < 40


def test_high_risk():
    risk = RiskEngine.calculate_risk(40, 10, 20)
    assert risk > 70

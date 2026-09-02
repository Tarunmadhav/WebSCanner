from webscanner.scoring.severity import risk_score

def test_risk_score():
    assert risk_score("high", "high") > risk_score("low", "high")
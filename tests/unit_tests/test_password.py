from app.passwords import validate_password

def test_strong():
    assert validate_password("Aa123456!!") == True

def test_weak():
    assert validate_password("password") == False
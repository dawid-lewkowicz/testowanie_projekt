from app.external_service import verify_vehicle_history

def test_verify_clean_vin():
    assert verify_vehicle_history("123ABC_CLEAN") is True

def test_verify_damaged_vin():
    assert verify_vehicle_history("123ABC_X") is False

def test_verify_vin_case_sensitivity():
    assert verify_vehicle_history("123ABC_x") is True
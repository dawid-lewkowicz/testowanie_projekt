def verify_vehicle_history(vin):
    if vin.endswith("X"): # auto z historią wypadkową 
        return False
    return True
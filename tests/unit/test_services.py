import pytest
from app import services
from datetime import datetime

@pytest.mark.parametrize("brand, model, year, price, vin", [
    ("BMW", "Seria 3", 2022, 220000, "123ABC_CLEAN"),
    ("Toyota", "Corolla", 2023, 115000, "123ABC_CLEAN"),
    ("Audi", "A6", 2020, 180000, "123ABC_CLEAN")
])
def test_add_car_success_scenarios(brand, model, year, price, vin):
    car_data = {
        "brand": brand, "model": model, "year": year, 
        "price": price, "vin": vin
    }
    
    result = services.add_car(car_data)

    assert len(services.cars_db) == 1
    assert result.brand == brand
    assert result.price == price
    assert result.vin == "123ABC_CLEAN"

@pytest.mark.parametrize("invalid_data, expected_error", [
    ({"price": -5000}, "Cena musi być większa niż zero"),
    ({"price": 0}, "Cena musi być większa niż zero"),
    ({"year": datetime.now().year + 2}, "Nieprawidłowy rok produkcji")
])
def test_add_car_validation_errors(invalid_data, expected_error):
    base_data = {
        "brand": "Ford", "model": "Focus", "year": 2020, 
        "price": 50000, "vin": "123ABC_CLEAN"
    }
    base_data.update(invalid_data)

    with pytest.raises(ValueError, match=expected_error):
        services.add_car(base_data)

def test_buy_car_success_flow(mocker):
    car = services.add_car({
        "brand": "Volvo", "model": "XC60", "year": 2021, 
        "price": 200000, "vin": "123ABC_CLEAN"
    })
    user = services.register_user({
        "username": "Dawid", "wallet_balance": 250000
    })

    mocker.patch("app.services.verify_vehicle_history", return_value=True)

    transaction = services.buy_car(user.id, car.id)

    assert transaction.final_price == 200000
    assert user.wallet_balance == 50000
    assert car.is_sold is True

def test_buy_car_fails_when_car_is_sold(mocker):
    car = services.add_car({
        "brand": "Mazda", "model": "6", "year": 2022, 
        "price": 140000, "vin": "123ABC_CLEAN"
    })
    user = services.register_user({
        "username": "Dawid", "wallet_balance": 200000
    })
    
    car.is_sold = True
    
    mocker.patch("app.services.verify_vehicle_history", return_value=True)

    with pytest.raises(ValueError, match="Auto jest już sprzedane"):
        services.buy_car(user.id, car.id)

def test_buy_car_fails_when_no_funds(mocker):
    car = services.add_car({
        "brand": "Mazda", "model": "6", "year": 2022, 
        "price": 140000, "vin": "123ABC_CLEAN"
    })
    user = services.register_user({
        "username": "Dawid", "wallet_balance": 200000
    })
    
    user.wallet_balance = 1000
    
    mocker.patch("app.services.verify_vehicle_history", return_value=True)

    with pytest.raises(ValueError, match="Niewystarczające środki na koncie"):
        services.buy_car(user.id, car.id)

def test_buy_car_stolen_vin(mocker):
    car = services.add_car({
        "brand": "Porsche", "model": "Cayenne", "year": 2023, 
        "price": 400000, "vin": "123ABC_X"
    })
    user = services.register_user({
        "username": "Dawid", "wallet_balance": 500000
    })

    mocker.patch("app.services.verify_vehicle_history", return_value=False)

    with pytest.raises(ValueError, match="Auto ma wypadkową historię"):
        services.buy_car(user.id, car.id)

def test_buy_car_user_not_found(mocker):
    car = services.add_car({
        "brand": "Fiat", "model": "Panda", "year": 2015, 
        "price": 15000, "vin": "123ABC_CLEAN"
    })
    
    mocker.patch("app.services.verify_vehicle_history", return_value=True)

    with pytest.raises(ValueError, match="Nie znaleziono użytkownika"):
        services.buy_car(999, car.id)

def test_buy_car_vehicle_not_found(mocker):
    user = services.register_user({
        "username": "Dawid", "wallet_balance": 50000
    })
    
    mocker.patch("app.services.verify_vehicle_history", return_value=True)

    with pytest.raises(ValueError, match="Nie znaleziono auta"):
        services.buy_car(user.id, 999)
import pytest
from app import services

@pytest.fixture(autouse=True)
def clean_db():
    services.cars_db = []
    services.users_db = []
    services.transactions_db = []

def test_add_car_success():
    car_data = {
        "brand": "BMW",
        "model": "3 series", 
        "year": 2021,
        "price": 200000, 
        "vin": "123ABC_CLEAN"
    }
    
    result = services.add_car(car_data)

    assert len(services.cars_db) == 1
    assert result.brand == "BMW"
    assert result.price == 200000

def test_add_car_invalid_price():
    car_data = {
        "brand": "BMW",
        "price": -100, 
        "year": 2021, 
        "vin": "123ABC_CLEAN",
        "model": "3 series"
    }
    
    with pytest.raises(ValueError, match="Cena musi być większa niż zero"):
        services.add_car(car_data)

def test_buy_car_success(mocker):
    car = services.add_car({
        "brand": "Audi",
        "model": "A4", 
        "year": 2019, 
        "price": 120000, 
        "vin": "VALID_VIN"
    })
    user = services.register_user({
        "username": "Janusz", "wallet_balance": 150000
    })

    mocker.patch("app.services.verify_vehicle_history", return_value=True)

    transaction = services.buy_car(user.id, car.id)

    assert transaction.final_price == 120000
    assert user.wallet_balance == 30000
    assert car.is_sold is True
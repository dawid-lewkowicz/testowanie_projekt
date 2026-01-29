from datetime import datetime
from app.models import Car, User, Transaction

def test_car_model_creation():
    car = Car(
        id=1,
        brand="BMW",
        model="M3",
        year=2023,
        price=350000,
        vin="123ABC_CLEAN"
    )
    
    assert car.id == 1
    assert car.brand == "BMW"
    assert car.price == 350000
    assert car.is_sold is False

def test_user_model_creation():
    user = User(
        id=1,
        username="Dawid",
        wallet_balance=150000.0
    )
    
    assert user.id == 1
    assert user.username == "Dawid"
    assert user.wallet_balance == 150000

def test_transaction_model_creation():
    now = datetime.now()
    transaction = Transaction(
        id=100,
        user_id=1,
        car_id=5,
        sale_date=now,
        final_price=340000
    )
    
    assert transaction.id == 100
    assert transaction.user_id == 1
    assert transaction.car_id == 5
    assert transaction.final_price == 340000
    assert transaction.sale_date == now

def test_car_default_value():
    car = Car(id=1, brand="Kia", model="Ceed", year=2020, price=50000, vin="123ABC_CLEAN")
    assert car.is_sold is False

def test_user_default_value():
    user = User(id=1, username="Dawid", wallet_balance=100)
    assert user.is_active is True
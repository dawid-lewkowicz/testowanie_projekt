from datetime import datetime
from typing import Dict, Optional
from app.models import Car, User, Transaction
from app.external_service import verify_vehicle_history

cars_db = []
users_db = []
transactions_db = []

def find_user_by_id(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    return None

def find_car_by_id(car_id):
    for car in cars_db:
        if car.id == car_id:
            return car
    return None

def add_car(data):
    price = data.get('price')
    year = data.get('year')
    current_year = datetime.now().year
 
    if price is None or price <= 0:
        raise ValueError("Cena musi być większa niż zero")
    
    if year is None or year > current_year:
        raise ValueError("Nieprawidłowy rok produkcji")

    new_car = Car(
        id=len(cars_db) + 1,
        brand=data.get('brand'),
        model=data.get('model'),
        year=year,
        price=price,
        vin=data.get('vin')
    )

    cars_db.append(new_car)
    return new_car


def register_user(data):
    new_user = User(
        id=len(users_db) + 1,
        username=data.get('username'),
        wallet_balance=data.get('wallet_balance', 0.0) # domyślnie 0
    )

    users_db.append(new_user)
    return new_user


def buy_car(user_id, car_id):
    user = find_user_by_id(user_id)
    car = find_car_by_id(car_id)

    if not user:
        raise ValueError("Nie znaleziono użytkownika")
    if not car:
        raise ValueError("Nie znaleziono auta")

    if car.is_sold:
        raise ValueError("Auto jest już sprzedane")

    if user.wallet_balance < car.price:
        raise ValueError("Niewystarczające środki na koncie")

    is_vehicle_clean = verify_vehicle_history(car.vin)
    if not is_vehicle_clean:
        raise ValueError("Auto ma wypadkową historię")

    user.wallet_balance -= car.price
    car.is_sold = True

    transaction = Transaction(
        id=len(transactions_db) + 1,
        car_id=car.id,
        user_id=user.id,
        sale_date=datetime.now(),
        final_price=car.price
    )

    transactions_db.append(transaction)
    return transaction
from dataclasses import dataclass # sam tworzy konstruktor __init__, widoczne dane w logach, łątwa zmiana obiektu na JSON, współpracuje z asdict
from datetime import datetime

@dataclass
class Car:
    id: int
    brand: str
    model: str
    year: int
    price: float
    vin: str
    is_sold: bool = False

@dataclass
class User:
    id: int
    username: str
    wallet_balance: float
    is_active: bool = True

@dataclass
class Transaction:
    id: int
    car_id: int
    user_id: int
    sale_date: datetime
    final_price: float
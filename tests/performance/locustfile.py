# locust -f tests/performance/locustfile.py
# http://localhost:8089

from locust import HttpUser, task, between
import random

class CarDealerUser(HttpUser):
    wait_time = between(1, 3)
    user_id = None
    wallet_balance = 10000000 

    real_cars_templates = [
        {"brand": "BMW", "model": "M3", "year": 2023, "price": 450000},
        {"brand": "Audi", "model": "RS6", "year": 2022, "price": 600000},
        {"brand": "Toyota", "model": "Corolla", "year": 2024, "price": 120000}
    ]

    def on_start(self):
        response = self.client.post("/users", json={
            "username": "Dawid",
            "wallet_balance": self.wallet_balance
        })
        if response.status_code in [200, 201]:
            self.user_id = response.json().get('id')

    @task(3)
    def view_cars_list(self):
        self.client.get("/cars")

    @task(2)
    def add_valid_car(self):
        car_data = random.choice(self.real_cars_templates).copy()
        car_data["vin"] = "123ABC_CLEAN"
        self.client.post("/cars", json=car_data)

    @task(2)
    def buy_available_car(self):
        if not self.user_id:
            return

        response = self.client.get("/cars")
        if response.status_code == 200:
            cars = response.json()
            available = [c for c in cars if not c.get('is_sold')]
            if available:
                target = random.choice(available)
                self.client.post(f"/buy/{self.user_id}/{target['id']}")
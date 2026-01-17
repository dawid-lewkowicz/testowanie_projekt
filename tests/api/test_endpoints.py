import pytest
from datetime import datetime

@pytest.mark.parametrize("brand, model, year, price, vin", [
    ("Mercedes", "CLA", 2022, 90000, "123ABC_CLEAN"),
    ("Fiat", "Punto", 2010, 5000, "123ABC_CLEAN"),
    ("Tesla", "Model S", 2024, 250000, "123ABC_CLEAN")
])
def test_create_car_success(client, brand, model, year, price, vin):
    payload = {
        "brand": brand, "model": model, "year": year, 
        "price": price, "vin": vin
    }
    response = client.post('/cars', json=payload)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['brand'] == brand
    assert data['price'] == price
    assert 'id' in data

@pytest.mark.parametrize("payload_update, expected_error", [
    ({"price": -100}, "Cena musi być większa niż zero"),
    ({"price": 0}, "Cena musi być większa niż zero"),
    ({"year": datetime.now().year + 2}, "Nieprawidłowy rok produkcji")
])
def test_create_car_invalid_data(client, payload_update, expected_error):
    base_payload = {
        "brand": "Test", "model": "Test", "year": 2020, 
        "price": 10000, "vin": "123ABC_CLEAN"
    }
    base_payload.update(payload_update)
    
    response = client.post('/cars', json=base_payload)
    
    assert response.status_code == 400
    assert expected_error in response.get_json()['error']


@pytest.mark.parametrize("car_price, car_vin, wallet, expected_error_fragment", [
    (5000, "123ABC_CLEAN", 100, "Niewystarczające środki"),
    (1000, "123ABC_X", 10000, "Auto ma wypadkową historię")
])
def test_buy_car_failures(client, car_price, car_vin, wallet, expected_error_fragment):
    car_res = client.post('/cars', json={
        "brand": "TestCar", "model": "FailCase", "year": 2020,
        "price": car_price, "vin": car_vin
    })
    car_id = car_res.get_json()['id']

    user_res = client.post('/users', json={
        "username": "Dawid", 
        "wallet_balance": wallet
    })
    user_id = user_res.get_json()['id']

    response = client.post(f'/buy/{user_id}/{car_id}')

    assert response.status_code == 400
    assert expected_error_fragment in response.get_json()['error']

def test_get_cars_list(client):
    client.post('/cars', json={
        "brand": "Porsche", "model": "911", "year": 2025, 
        "price": 1000000, "vin": "123ABC_CLEAN"
    })
    response = client.get('/cars')
    assert response.status_code == 200
    assert len(response.get_json()) >= 1

def test_buy_car_success_flow(client):
    c = client.post('/cars', json={"brand": "Opel", "model": "Astra", "year": 2010, "price": 1000, "vin": "123ABC_CLEAN"}).get_json()
    u = client.post('/users', json={"username": "Dawid", "wallet_balance": 2000}).get_json()
    
    res = client.post(f'/buy/{u["id"]}/{c["id"]}')
    
    assert res.status_code == 200
    assert res.get_json()['transaction']['final_price'] == 1000
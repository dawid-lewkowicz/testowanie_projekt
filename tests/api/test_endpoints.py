import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True # tryb testowy, błędy są lepiej opisane
    with app.test_client() as client: # wirtualny klient, bez uruchamiania serwera na porcie 5000
        yield client

def test_create_car_endpoint(client):
    payload = {
        "brand": "Mercedes", 
        "model": "CLA", 
        "year": 2022, 
        "price": 90000, 
        "vin": "123ABC_CLEAN"
    }
    response = client.post('/cars', json=payload)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['brand'] == "Mercedes"
    assert 'id' in data

def test_get_cars_list(client):
    client.post('/cars', json={
        "brand": "Porsche", "model": "911 GT3",
        "price": 1500000, "year": 2025, "vin": "123ABC_CLEAN"
    })
    response = client.get('/cars')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
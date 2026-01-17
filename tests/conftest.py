import pytest
from app.main import app
from app import services

# Globalne fixture dla wszystkich testów

@pytest.fixture
def client():
    app.config['TESTING'] = True # tryb testowy, błędy są lepiej opisane
    with app.test_client() as client: # wirtualny klient, bez uruchamiania serwera na porcie 5000
        yield client

@pytest.fixture(autouse=True)
def clean_db():
    services.cars_db = []
    services.users_db = []
    services.transactions_db = []
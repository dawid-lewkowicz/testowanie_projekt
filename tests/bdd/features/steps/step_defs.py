from behave import given, when, then
from app import services
from app.models import Car, User

@given('Mamy dostępne auto marki "{brand}" o cenie {price:d} i VIN "{vin}"')
def step_impl(context, brand, price, vin):
    services.cars_db = []
    context.car = services.add_car({
        "brand": brand, "model": "Test", "year": 2020, 
        "price": price, "vin": vin
    })

@given('Mamy użytkownika "{username}" z portfelem {balance:d}')
def step_impl(context, username, balance):
    services.users_db = []
    context.user = services.register_user({
        "username": username, "wallet_balance": balance
    })

@when('Użytkownik kupuje to auto')
def step_impl(context):
    context.transaction = services.buy_car(context.user.id, context.car.id)

@then('Auto zostaje oznaczone jako sprzedane')
def step_impl(context):
    assert context.car.is_sold is True

@then('Stan konta użytkownika wynosi {balance:d}')
def step_impl(context, balance):
    assert context.user.wallet_balance == balance
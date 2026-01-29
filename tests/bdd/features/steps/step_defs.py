from behave import given, when, then
from app import services

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
    try:
        context.transaction = services.buy_car(context.user.id, context.car.id)
        context.error = None 
    except ValueError as e:
        context.error = str(e)

@then('Auto zostaje oznaczone jako sprzedane')
def step_impl(context):
    assert context.car.is_sold is True

@then('Auto nie zostaje oznaczone jako sprzedane')
def step_impl(context):
    assert context.car.is_sold is False

@then('Stan konta użytkownika wynosi {balance:d}')
def step_impl(context, balance):
    assert context.user.wallet_balance == balance

@then('Operacja kończy się błędem "{message}"')
def step_impl(context, message):
    assert context.error is not None, "Oczekiwano błędu, ale operacja się powiodła"
    assert context.error == message

@when('Użytkownik sprawdza listę aut')
def step_impl(context):
    context.car_list = services.cars_db

@then('Na liście znajduje się auto marki "{brand}"')
def step_impl(context, brand):
    found = False
    for car in context.car_list:
        if car.brand == brand:
            found = True
            break
    assert found is True
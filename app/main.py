from flask import Flask, request, jsonify
from app import services
from dataclasses import asdict

app = Flask(__name__)

@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    try:
        car = services.add_car(data)
        return jsonify(asdict(car)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": f"Brak pola: {str(e)}"}), 400

@app.route('/cars', methods=['GET'])
def list_cars():
    lista_wynikowa = []

    for auto_obiekt in services.cars_db:
        auto_slownik = asdict(auto_obiekt)
        lista_wynikowa.append(auto_slownik)

    return jsonify(lista_wynikowa), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = services.register_user(data)
        return jsonify(asdict(user)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/buy/<int:user_id>/<int:car_id>', methods=['POST'])
def purchase_car(user_id, car_id):
    try:
        transaction = services.buy_car(user_id, car_id)
        trans_dict = asdict(transaction)
        trans_dict['sale_date'] = trans_dict['sale_date'].isoformat() # JSON nie obsługuje typu datetime, więc zmieniamy na stringa
        
        return jsonify({"message": "Zakup udany!", "transaction": trans_dict}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
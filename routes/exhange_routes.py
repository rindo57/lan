from flask import Blueprint, request, jsonify
from models import mongo, create_language_exchange

exchange_bp = Blueprint('exchange_bp', __name__)

# Request a language exchange
@exchange_bp.route('/request', methods=['POST'])
def request_exchange():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data"}), 400

    # Ensure users exist
    user1 = mongo.db.users.find_one({"_id": mongo.ObjectId(data['user_id1'])})
    user2 = mongo.db.users.find_one({"_id": mongo.ObjectId(data['user_id2'])})

    if not user1 or not user2:
        return jsonify({"message": "User(s) not found"}), 404

    # Create the exchange request
    exchange = create_language_exchange(
        data['user_id1'],
        data['user_id2'],
        data['language1'],
        data['language2']
    )

    mongo.db.language_exchanges.insert_one(exchange)
    return jsonify({"message": "Exchange request sent"}), 201

# Get language exchanges for a specific user
@exchange_bp.route('/<user_id>', methods=['GET'])
def get_user_exchanges(user_id):
    exchanges = mongo.db.language_exchanges.find({
        '$or': [{'user_id1': user_id}, {'user_id2': user_id}]
    })
    exchange_list = []
    for exchange in exchanges:
        exchange_list.append({
            'user_id1': exchange['user_id1'],
            'user_id2': exchange['user_id2'],
            'language1': exchange['language1'],
            'language2': exchange['language2'],
            'status': exchange['status'],
            'dateCreated': exchange['dateCreated']
        })

    return jsonify(exchange_list), 200

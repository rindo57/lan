from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import mongo, bcrypt, create_user

user_bp = Blueprint('user_bp', __name__)

# Register a new user
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data"}), 400

    # Check if user already exists
    existing_user = mongo.db.users.find_one({"email": data['email']})
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # Create new user
    user = create_user(
        data['username'],
        data['email'],
        data['password'],
        data['languages'],
        data['learning_languages'],
        data['bio'],
        data['location']
    )

    mongo.db.users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

# Login user and generate JWT token
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data"}), 400

    # Find user by email
    user = mongo.db.users.find_one({"email": data['email']})
    if not user or not bcrypt.check_password_hash(user['password_hash'], data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({"access_token": access_token}), 200

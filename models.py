from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

# User model
def create_user(username, email, password, languages, learning_languages, bio, location):
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'languages': languages,
        'learning_languages': learning_languages,
        'profile': {'bio': bio, 'location': location}
    }
    return user

# Language Exchange request model
def create_language_exchange(user_id1, user_id2, language1, language2):
    return {
        'user_id1': user_id1,
        'user_id2': user_id2,
        'language1': language1,
        'language2': language2,
        'status': 'pending',  # Pending, accepted, rejected
    }

from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager
from models import mongo, bcrypt
from routes.user_routes import user_bp
from routes.exchange_routes import exchange_bp

app = Flask(__name__)

# Load configurations
app.config.from_object(Config)

# Initialize extensions
mongo.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Register Blueprints (Routes)
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(exchange_bp, url_prefix='/api/exchanges')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)

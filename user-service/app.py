from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flasgger import Swagger
from sqlalchemy.exc import IntegrityError
from prometheus_flask_exporter import PrometheusMetrics
from dotenv import load_dotenv
import os

# env_path = '../.env' # Local Testing
env_path = '.env' # Docker Container
load_dotenv(env_path)  # Load environment variables from the .env file

# Now you can access your variables
postgres_user = os.getenv('DB_USERNAME')
postgres_password = os.getenv('DB_PASSWORD')

print("Postgres User:", postgres_user)
print("Postgres Password:", postgres_password)


app = Flask(__name__)
swagger = Swagger(app)

# Local Host
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://new_user:new_password@localhost/trivia_game'

# Docker Compose
SQLALCHEMY_DATABASE_URI = f'postgresql://{postgres_user}:{postgres_password}@postgres:5432/trivia_game'
print(SQLALCHEMY_DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI


app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this!

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Enable Prometheus Metrics
metrics = PrometheusMetrics(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/api/register', methods=['POST'])
def register_user():
    """
    User Registration
    ---
    parameters:
      - name: username
        type: string
        required: true
        description: The username of the user.
      - name: password
        type: string
        required: true
        description: The password of the user.
    responses:
      201:
        description: User registered successfully.
      400:
        description: Username already exists.
    """
    data = request.get_json()

    if not data or not all(k in data for k in ("username", "password")):
        return jsonify({"message": "Missing data"}), 400
    
    new_user = User(username=data['username'], password=data['password'])  # Password hashing should be added
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "User with that username or email already exists"}), 409


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()  # Password checking should be added
    if user:
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401


# Endpoint to get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [{"id": user.id, "username": user.username, "password": user.password} for user in users]
    return jsonify(users_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/trivia_game'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://new_user:new_password@localhost/trivia_game'

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this!

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
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
    new_user = User(username=data['username'], password=data['password'])  # Password hashing should be added
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()  # Password checking should be added
    if user:
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5001)

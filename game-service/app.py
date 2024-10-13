from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
swagger = Swagger(app)
# Local Host
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://new_user:new_password@localhost/trivia_game'

# Docker Compose
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://new_user:new_password@postgres:5432/trivia_game'
db = SQLAlchemy(app)

# Enable Prometheus Metrics
metrics = PrometheusMetrics(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(50), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/api/create_game', methods=['POST'])
@jwt_required()
def create_game():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_game = Game(question=data['question'], correct_answer=data['correct_answer'])
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game created successfully'}), 201

@app.route('/api/get_games', methods=['GET'])
@jwt_required()
def get_games():
    games = Game.query.all()
    return jsonify([{'id': game.id, 'question': game.question, 'correct_answer': game.correct_answer} for game in games]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

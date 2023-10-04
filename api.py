from flask import Blueprint, request, jsonify
from models import User
from database import db

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.username for user in users]), 200

@api.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'username': user.username, 'message': user.message}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    message = data.get('message', '')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, message=message)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'username': new_user.username, 'message': new_user.message}), 201

@api.route('/users/<username>', methods=['PUT'])
def update_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    message = data.get('message', '')

    user.message = message
    db.session.commit()

    return jsonify({'username': user.username, 'message': user.message}), 200

@api.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return '', 204

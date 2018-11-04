# From: Creating a RESTFul API in Flask With JSON Web Token Authentication and Flask-SQLAlchemy
# ref : https://www.youtube.com/watch?v=WxGBoY5iNXY

from flask import Blueprint, request, jsonify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from lib.utils import token_required, route_info

from db.database import db_session
from db.models_demo import User

prefix = 'demo'
mod = Blueprint(prefix, __name__)



@mod.route('/', methods=['GET'])
def index():
    """API列表 (＊Token required )"""
    return route_info(prefix)



@mod.route('/users', methods=['GET'])
@token_required
def get_all_user():
    """＊ Get all users """
    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['name'] = user.name
        user_data['public_id'] = user.public_id
        user_data['password']  = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
        
    return jsonify({'message': output})



@mod.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_users(public_id):
    """＊ Get one user """
    user = User.query.filter_by(public_id = public_id).first()

    if not user:
        return jsonify({'message': 'User not found'})
    
    user_data = {}
    user_data['name'] = user.name
    user_data['public_id'] = user.public_id
    user_data['password']  = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})



@mod.route('/create-user', methods=['POST'])
@token_required
def create_user():
    """＊ Create An user """    
    data =  request.get_json()

    hash_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hash_password, admin=False)
    
    db_session.add(new_user)
    db_session.commit()

    return jsonify({'message': 'Create a new user.'})



@mod.route('/promote-user/<public_id>', methods=['PUT'])
@token_required
def promote_user(public_id):
    """＊ Promote An user """    
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found'})
    
    user.admin = True
    db_session.commit()

    return get_one_users(user.public_id)



@mod.route('/delete-user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(public_id):
    """＊ Delete An user """    
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found'})
    
    db_session.delete(user)
    db_session.commit()

    return jsonify({'message': 'Delete one record!'})
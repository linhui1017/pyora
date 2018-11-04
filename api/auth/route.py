from flask import Blueprint, request, make_response, jsonify

from settings import Config
from lib.utils import route_info

import jwt
import datetime


prefix = 'auth'
mod = Blueprint(prefix, __name__)

@mod.route('/', methods=['GET'])
def index():
    """API列表"""
    return route_info(prefix)

@mod.route('/login', methods=['GET'])
def login():
    """JWT 基本帳號密碼認帳"""
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic relm="Login required!"'})

    if auth.username == Config.AUTH_USER and auth.password == Config.AUTH_PASSWORD:
        token = jwt.encode({'user_id': Config.AUTH_USER, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15) }, Config.SECRET_KEY)
        return jsonify({'status': '200', 'message': 'OK', 'token': token.decode('UTF-8')})
    
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic relm="Login required!"'})

from flask import Blueprint, request

from lib.utils import token_required, route_info

from  api.test import get_all_users, get_user

prefix = 'test'
mod = Blueprint(prefix, __name__)

@mod.route('/', methods=['GET'])
def index():
    """API列表 (＊Token required )"""
    return route_info(prefix)

@mod.route('/alluser', methods=['GET'])
def _get_all_user():
    return get_all_users.run()

@mod.route('/user', methods=['GET'])
def _get_user():
    return get_user.run()


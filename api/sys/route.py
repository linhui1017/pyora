from flask import Blueprint, request

from lib.utils import token_required, route_info

from  api.sys import get_hostname,  get_oradatetime, po_dataProvider, po_sqlProxy

prefix = 'sys'
mod = Blueprint(prefix, __name__)

@mod.route('/', methods=['GET'])
def index():
    """API列表 (＊Token required )"""
    return route_info(prefix)

@mod.route('/ora-hostname', methods=['GET'])
def _get_hostname():
    """資料庫主機名稱"""
    return get_hostname.run()

@mod.route('/ora-sysdatetime', methods=['GET'])
def _get_oradatetime():
    """資料庫主機系統時間"""
    return get_oradatetime.run()


@mod.route('/data-provider', methods=['POST'])
@token_required
def _po_dataProvider():
    """＊資料提供模組"""
    return po_dataProvider.run()

@mod.route('/sql-proxy', methods=['POST'])
@token_required
def _po_sqlProxy():
    """＊資料提供模組：參考KFSYSCC.SYSQRYM"""
    return po_sqlProxy.run()

'''
@mod.route('/sysuser', methods=['GET'])
@token_required
def _get_all_users():
    """＊全部使用者"""
    return get_all_users.run()

@mod.route('/sysuser/<user_id>', methods=['GET'])
@token_required
def _get_one_user(user_id):
    """＊指定單一使用者"""
    return get_one_user.run(user_id)

@mod.route('/updateNeoName', methods=['GET'])
def _po_updateNeoName():
#    """資料庫異動資料測試含交易成功"""
    return po_updateNeoName.run()
   

@mod.route('/updateUserName', methods=['POST'])
def _po_updateUserName():
    """資料庫異動資料測試含交易成功"""
    return po_updateUserName.run()
'''   
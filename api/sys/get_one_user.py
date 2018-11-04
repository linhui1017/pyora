from flask import jsonify

import json
from db.dbora import Query
from lib.utils import api_response


def run(user_id):
    
    sql = """ SELECT * FROM SYSUSER WHERE USER_ID=:user_id  """

    params = {}
    params['user_id'] = user_id
    rs = Query(sql, **params)    

    return api_response(**rs)


from flask import request, jsonify
import json
from db.dbora import Query
from lib.utils import api_response

def run():
    try:
        content = request.get_json()

        if request.is_json == False:
            return jsonify({'status':401, 'message': 'JSON request required.'}), 401   

        sql = content['CommandText']
        params = content['Parameters']

        rs = Query(sql, **params)    

        return api_response(**rs)

    except Exception as e:
        return jsonify({'status':400, 'message': str(e)})
   
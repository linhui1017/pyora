#from flask import jsonify -- performance < json.dumps
import json
from flask import jsonify
from flask import Response

from db.database import pg_session, models_to_list
from lib.utils import api_response
from entity.LineProfileEntity import LineProfile

def run():
    try:
        users = pg_session.query(LineProfile) \
        .filter(LineProfile.USER_ID == 'aaaa') \
        .all()

        result = models_to_list(users)
        rs = {'status':200, 'message': 'OK', 'data': result}
        return api_response(**rs)
    except Exception as e:
        error, = e.args
        rs = {'status':404, 'message': error.message, 'data': []}
        return api_response(**rs)
    finally:
        pg_session.close()



   

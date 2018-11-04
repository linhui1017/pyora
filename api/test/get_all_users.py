#from flask import jsonify -- performance < json.dumps
import json
from flask import Response

from db.dbpg import Query
from lib.utils import api_response

def run():
    # sql = """
    #    SELECT * FROM public."LINE_PROFILE" WHERE "USER_ID" = %(user_id)s
    # """

    sql = """
       SELECT A.*, current_timestamp as dt FROM public."LINE_PROFILE" A WHERE A."USER_ID" = :user_id
    """
    params = {}
    params['user_id'] = 'aaaa'
    rs = Query(sql, **params) 

    return api_response(**rs)

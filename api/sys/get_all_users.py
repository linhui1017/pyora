#from flask import jsonify -- performance < json.dumps
import json
from flask import Response

from db.dbora import Query
from lib.utils import api_response

def run():
    sql = """
       SELECT USER_ID, USER_NAME, USER_ENG_NAME, DEPT_CODE FROM SYSUSER
    """
    rs = Query(sql)
    return api_response(**rs)

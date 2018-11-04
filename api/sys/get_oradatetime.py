import json

from db.dbora import Query
from lib.utils import api_response

def run():
    sql = """
        SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') "Now" FROM DUAL
    """
    rs = Query(sql)
    return api_response(**rs)


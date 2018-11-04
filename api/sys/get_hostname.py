import json

from db.dbora import Query
from lib.utils import api_response

def run():
    sql = """
        SELECT FN_HOSTNAME() "Host" FROM DUAL
    """
    rs = Query(sql)

    return api_response(**rs)


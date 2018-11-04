from flask import request
import json
from db.dbora import StartTransaction, Commit, Rollback, ExecSQL
from lib.utils import api_response

import xmltodict

def run():
    try:
        params = request.get_json()

        if not params:
            return {'status':400, 'message': 'Posted data not matched!'}   

        conn = StartTransaction()

        rs = ExecSQL(conn,
        '''
           UPDATE KFSYSCC.SYSUSER
           SET USER_NAME=:userName
           WHERE USER_ID=:userId
        '''
        , **params
        )

        if rs['status'] != 200:
            Rollback(conn)
            return api_response(**rs)

        rs = Commit(conn)
        
        return api_response(**rs)

    except:
        raise
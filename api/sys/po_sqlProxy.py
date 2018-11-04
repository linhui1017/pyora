from flask import request, jsonify
import json
from db.dbora import Query, StartTransaction, ExecSQL, Rollback, Commit
from lib.utils import api_response

def run():
    try:
        if request.is_json == False:
            return jsonify({'status':401, 'message': 'JSON request required.'}), 401   

        content = request.get_json()

        cmd = content['CommandText']
        params = {}
        params['cmd'] = cmd

        sql = """ SELECT QRY_SQL||QRY_SQL2||QRY_SQL3 QRY_SQL FROM SYSQRYM WHERE UPPER(PXY_CMD) = UPPER(:cmd) AND QRY_VALID='Y' AND GRP_ID='WS' """

        rs = Query(sql, **params)  

        if rs['status'] != 200:
            return  jsonify({'status': rs['status'], 'message': rs['message']})

        if not rs['data']:
            return  jsonify({'status': 401, 'message': 'SQL not found.'})

        data = rs['data'][0]
        sql = data['QRY_SQL']
        sql = sql.replace("\r\n", " ")

        params = {}
        params = content['Parameters']

        tmpSQL = sql.upper()
        if ('INSERT ' in tmpSQL) or ('UPDATE ' in tmpSQL) or ('DELETE ' in tmpSQL):
            try:
                conn = StartTransaction()
                rs = ExecSQL(conn, sql, **params)

                if rs['status'] != 200:
                    Rollback(conn)
                    return api_response(**rs)

                rs = Commit(conn)                
            except:
                raise        
        else:
            rs = Query(sql, **params)  

        return api_response(**rs)

    except Exception as e:
        return jsonify({'status':400, 'message': str(e)})
   
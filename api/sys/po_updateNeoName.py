
from db.dbora import StartTransaction, Commit, Rollback, ExecSQL
from lib.utils import api_response

def run():
    
    try:
        conn = StartTransaction()

        Params = {}
        Params['USER_ID'] = '002057'
        Params['USER_NAME'] = 'Marry'

        rs = ExecSQL(conn,
        '''
            UPDATE SYSUSER SET USER_NAME=:USER_NAME WHERE USER_ID=:USER_ID
        '''
        , **Params
        )

        if rs['status'] != 200:
            Rollback(conn)
            return api_response(**rs)

        Params = {}
        #Params['USER_ID'] = '002057'
        #Params['USER_NAME'] = '林俊偉'

        rs = ExecSQL(conn,
        '''
           INSERT INTO SURVEY1ANS(ID) VALUES(9)
        '''
        , **Params
        )

        if rs['status'] != 200:
            Rollback(conn)
            return api_response(**rs)

        rs = Commit(conn)

        return api_response(**rs)

    except:
        raise

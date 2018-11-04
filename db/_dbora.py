import cx_Oracle
import json

from datetime import datetime
from flask import jsonify
from collections import namedtuple
from db.database import pool

# Type Convert
def Convert(value):
    if type(value) is cx_Oracle.LOB:
        return value.read()
    elif type(value) is cx_Oracle.DATETIME:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif type(value) is datetime:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    else: 
        return value

# Dict
def Query(sql, **params):
    try:
        conn = pool.acquire()
        cur = conn.cursor()
        cur.execute(sql, params)
        data =  [dict((cur.description[i][0], Convert(value)) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
        return {'status':200, 'message': 'OK', 'data': data}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return {'status':404, 'message': error.message, 'data': []}
    finally:
        cur.close()
        conn.close()

# NamedTuple
def QueryN(sql, **params):
    try:
        conn = pool.acquire()
        cur = conn.cursor()
        cur.execute(sql, params)
        columnNames = [col[0] for col in cur.description]
        RowType = namedtuple('Row', columnNames)
        data = [RowType(*row) \
            for row in cur.fetchall() ]

        return data
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return {'status':404, 'message:': error.message}
    finally:
        cur.close()        
        conn.close()

# Start Transaction
def StartTransaction():
    try:
        conn = pool.acquire()
        conn.begin()
        return conn
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print('oracle error:{0}'.format(error.message))
        raise

# Rollback Transaction
def Rollback(conn):
    try:
        conn.rollback()
        conn.close()
        return {'status':200, 'message':'OK'}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print('oracle error:{0}'.format(error.message))
        conn.close()
        return {'status':400, 'message': error.message}        

# Commit Transaction
def Commit(conn):
    try:
        conn.commit()
        conn.close()
        return {'status':200, 'message':'OK'}
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print('oracle error:{0}'.format(error.message))
        conn.rollback()
        conn.close()
        return {'status':400, 'message': error.message}   
         
# Execute
def ExecSQL(conn, sql, **params):
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        return {'status':200, 'message':'OK'}        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print('oracle error:{0}'.format(error.message))
        return {'status':400, 'message': error.message}                

    

    






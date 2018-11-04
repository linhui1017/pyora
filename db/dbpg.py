import psycopg2
import json
import sqlalchemy
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.sql import text

from datetime import datetime
from flask import jsonify
from collections import namedtuple
from db.database import pg_session
import logging


# Type Convert
def Convert(value):
    if type(value) is datetime:
            return value.strftime("%Y-%m-%d %H:%M:%S")
    else: 
        return value

# Dict
# def Query(sql, **params):
#     try:
#         conn= pool.getconn()
#         cur =conn.cursor()
#         cur.execute(sql, params)
#         data =  [dict((cur.description[i][0], Convert(value)) \
#                for i, value in enumerate(row)) for row in cur.fetchall()]
#         return {'status':200, 'message': 'OK', 'data': data}
#     except psycopg2.Error as e:
#         error, = e.args
#         return {'status':404, 'message': error.message, 'data': []}
#     finally:
#         cur.close()
#         pool.putconn(conn)

# Dict

def Query(sql, **params):
    try:
        comment = text(sql)
        session = pg_session()
        proxy =  session.execute(comment, params)
        descrip = proxy._cursor_description()
        cur = proxy.fetchall()
        data =  [dict((descrip[i][0], Convert(value)) \
               for i, value in enumerate(row)) for row in cur]
 
        return {'status':200, 'message': 'OK', 'data': data}
    except sqlalchemy.exc.SQLAlchemyError as e:
        error, = e.args
        logging.error(error)
        return {'status':404, 'message': error, 'data': []}
    finally:
        session.close()
     
     
# Start Transaction
def StartTransaction():
    try:
        session = pg_session()
        return session
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        print('pgdb error:{0}'.format(error))
        raise

# Rollback Transaction
def Rollback(trans):
    try:
        trans.rollback()
        trans.close()
        return {'status':200, 'message':'OK'}
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        print('pgdb error:{0}'.format(error))
        trans.close()
        return {'status':400, 'message': error}        

# Commit Transaction
def Commit(trans):
    try:
        trans.commit()
        trans.close()
        return {'status':200, 'message':'OK'}
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        print('pgdb error:{0}'.format(error))
        trans.rollback()
        trans.close()
        return {'status':400, 'message': error}   
         
# Execute
def ExecSQL(trans, sql, **params):
    try:
        comment = text(sql)
        proxy =  trans.execute(comment, params)
        return {'status':200, 'message':'OK'}        
    except sqlalchemy.exc.DatabaseError as e:
        error, = e.args
        print('pgdb error:{0}'.format(error))
        return {'status':400, 'message': error}  

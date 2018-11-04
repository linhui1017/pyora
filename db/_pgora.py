import psycopg2
import json

from datetime import datetime
from flask import jsonify
from collections import namedtuple
from db.PostgersDB import pool

# Type Convert
def Convert(value):
    if type(value) is datetime:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    else: 
        return value

# Dict
def Query(sql, **params):
    try:
        conn= pool.getconn()
        cur =conn.cursor()
        cur.execute(sql, params)
        data =  [dict((cur.description[i][0], Convert(value)) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
        return {'status':200, 'message': 'OK', 'data': data}
    except psycopg2.Error as e:
        error, = e.args
        return {'status':404, 'message': error.message, 'data': []}
    finally:
        cur.close()
        pool.putconn(conn)
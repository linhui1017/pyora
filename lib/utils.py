from flask import jsonify, request, Response
from flask import current_app as app
from functools import wraps
import dicttoxml

import json
import jwt
from datetime import datetime

from settings import Config, Message

# API usage document via FLASK
def route_info(prefix):
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            if (prefix == None) or ("/{}/".format(prefix) in rule.rule):
                func_list[rule.rule] = "[{}]:{}".format(rule.methods, app.view_functions[rule.endpoint].__doc__)

    return jsonify(func_list)

# JWT authenticated decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if Config.TOKEN_REQUIRED:
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'status':401, 'message': Message.TOKEN_IS_MISING}), 401

            try:
                data = jwt.decode(token, Config.SECRET_KEY)

                if not ( data['user_id'] == Config.AUTH_USER ):
                    return jsonify({'status':401, 'message': Message.TOKEN_IS_MISING}), 401     
            except:
                return jsonify({'status':401, 'message': Message.TOKEN_IS_MISING}), 401 

        return f(*args, **kwargs)
    return decorated

def jsonconverter(o):
    if isinstance(o, datetime):
        #return o.__str__()
        return o.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return o

# api response format
def api_response(**data):

    if not data:
        return jsonify({'status':400, 'message': 'Posted data not matched!'})

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/xml') or (content_type == 'text/xml'):
        #return Response(dict2XML(data, utf8=True).decode("utf-8"), mimetype='application/xml')
        return Response(dicttoxml.dicttoxml(data), mimetype='application/xml')
    else:
        return Response(json.dumps(data, default = jsonconverter, ensure_ascii=False), mimetype='application/json') 

# AES 
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES 

 # Bytes
BLOCK_SIZE = 16 
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """
    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('utf8') 
        
from sqlalchemy.orm import class_mapper

def to_dict(self):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(self.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(self, c)) for c in columns)


def models_to_list(models):
    
    if models is not None and  isinstance(models, list):
        result = []
        for model in models:
            if hasattr(model, 'to_dict'):
                result.append(model.to_dict()) 
        return result
    elif models is not None and hasattr(models, 'to_dict'): 
        return models.to_dict()
    else:
        return None

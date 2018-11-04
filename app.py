from flask import Flask
from flask_cors import CORS

from lib import utils, logs
from settings import Config
import logging


app = Flask(__name__)

logs.initialize_log()


CORS(app)

# Config
app.config.from_object(Config)

logging.info('SERVER initialize')

def initialize_route(flask_app):
    from api.test.route import mod as pgmod
    flask_app.register_blueprint(pgmod, url_prefix='/api/test')


initialize_route(app)

""" 
  To use SQLAlchemy in a declarative way with your application,
  you just have to put the following code into your application module. 
  Flask will automatically remove database sessions at the end of the request
   or when the application shuts down
"""



@app.route('/api')
def help():
    """所有API列表"""
    return utils.route_info(None)

   

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='172.21.42.7', port=5000)
    #app.run(debug=Config.DEBUG)
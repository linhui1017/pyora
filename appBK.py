from flask import Flask
from flask_cors import CORS

from lib import utils
from settings import Config

app = Flask(__name__)
CORS(app)

# Config
app.config.from_object(Config)

def initialize_route(flask_app):
    from api.sys.route import mod as sysmod
    flask_app.register_blueprint(sysmod, url_prefix='/sys')
 
#    from api.demo.route import mod as demomod
#    flask_app.register_blueprint(demomod, url_prefix='/demo')
 
    from api.auth.route import mod as authmod
    flask_app.register_blueprint(authmod, url_prefix='/auth')

#    from api.iac.route import mod as iacmod
#    flask_app.register_blueprint(iacmod, url_prefix='/iac')


initialize_route(app)

""" 
  To use SQLAlchemy in a declarative way with your application,
  you just have to put the following code into your application module. 
  Flask will automatically remove database sessions at the end of the request
   or when the application shuts down
"""

from db.database import db_session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def help():
    """所有API列表"""
    return utils.route_info(None)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='172.21.42.7', port=5000)
    #app.run(debug=Config.DEBUG)
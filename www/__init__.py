from flask import Flask,jsonify,render_template,request,url_for,redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import platform
import netifaces as ni
from flask_bcrypt import Bcrypt
import json
# 

#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fs0ci3ty'
# Flask Bcrypt
bcrypt = Bcrypt(app) #
candidate = 'secret' #
# IP
ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] # Linux 
# DB
engine = create_engine('mysql+mysqldb://root:gcc@2k20~#@db:3306/db_sfsp',pool_size=1000, max_overflow=0)
db = scoped_session(sessionmaker(bind=engine))

#### Maintenance ####
is_maintenance_mode = False

# Always throw a 503 during maintenance: http://is.gd/DksGDm

@app.before_request
def check_for_maintenance():
    if is_maintenance_mode and request.path != url_for('maintenance'): 
        return redirect('/maintenance')
        # Or alternatively, dont redirect 
        # return 'Sorry, off for maintenance!', 503

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')
########################

## 404 Page Not Found ##
@app.errorhandler(404)
def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404
########################
from www.user import ubv
from www.admin import abv
app.register_blueprint(ubv,url_prefix="/user")
app.register_blueprint(abv,url_prefix="/admin")
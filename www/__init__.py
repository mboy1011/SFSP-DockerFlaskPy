from flask import Flask,jsonify
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
# Views
from www.view import ubv
from www.admin import abv
app.register_blueprint(ubv,url_prefix="/")
app.register_blueprint(abv,url_prefix="/")
from flask import render_template,session,redirect,url_for,request,session,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import json
# MySQL Database
engine = create_engine('mysql+mysqldb://root:gcc@2k20~#@db:3306/db_queuing',pool_size=1000, max_overflow=0)
db = scoped_session(sessionmaker(bind=engine))

class View:    
    def index():
        # return f'''{status}'''
        return render_template('index.html')

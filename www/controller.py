from flask import Flask,render_template,session,redirect,url_for,request,session,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import platform
import netifaces as ni
from flask_bcrypt import Bcrypt
import json

#
app = Flask(__name__)
# Flask Bcrypt
bcrypt = Bcrypt(app) #
candidate = 'secret' #
# IP
ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] # Linux 
# DB
engine = create_engine('mysql+mysqldb://root:gcc@2k20~#@db:3306/db_sfsp',pool_size=1000, max_overflow=0)
db = scoped_session(sessionmaker(bind=engine))
# Views
class View:  
    @app.route('/')    
    def index():
        # return f'''{status}'''
        return render_template('index.html')

    @app.route('/login',methods=['POST'])
    def login():
        mail = request.form['email']
        passwd = request.form['pass']
        query = db.execute(f"SELECT u_email, u_pass FROM tbl_user_accounts WHERE u_email='{mail}'")
        result = query.fetchone()
        hashed = result[1]
        # pw_hash = bcrypt.generate_password_hash(passwd)
        if bcrypt.check_password_hash(hashed, passwd):
            return f'''Matched!'''
        else:
            return f'''Not matched!'''
        # return f'''{pw_hash}'''
        # hashed
    @app.route('/admin')
    def admin():
        return render_template('admin.html')

if __name__ == "__main__":
    View()
    # Flask
    FLASK_APP="main"
    Flask.run(app,debug=True,host=ip,port=5000,threaded=True)
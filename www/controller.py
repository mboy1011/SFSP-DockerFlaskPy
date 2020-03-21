from flask import Flask,render_template,session,redirect,url_for,request,session,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import platform
import netifaces as ni
from flask_bcrypt import Bcrypt
import json

#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fs0ci3ty'
# Flask Bcrypt
bcrypt = Bcrypt(app) #
candidate = 'secret' #
# IP
ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] # Linux 
# DB
engine = create_engine('mysql+mysqldb://root:gcc@2k20~#@db:6033/db_sfsp',pool_size=1000, max_overflow=0)
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
        query = db.execute(f"SELECT u_email, u_pass,u_type FROM tbl_user_accounts WHERE u_email='{mail}'")
        result = query.fetchone()
        # pw_hash = bcrypt.generate_password_hash(passwd)
        # return f"{pw_hash}"
        if result:
            hashed = result[1]
            # pw_hash = bcrypt.generate_password_hash(passwd)
            if bcrypt.check_password_hash(hashed, passwd):
                session['userType'] = result[2]
                session['userEmail'] = result[0]
                return redirect('/admin')
            else:
                status = "Invalid Username/Password!"
                return render_template('index.html',status=status)
        else:
            status = "Invalid Username/Password!"
            return render_template('index.html',status=status)
    @app.route('/admin')
    def admin():
        if 'userType' in session:
            if session['userType']==1:
                return render_template('admin.html')
            else:
                return redirect('/')
        else:
            return redirect('/')
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')

if __name__ == "__main__":
    View()
    # Flask
    FLASK_APP="main"
    Flask.run(app,debug=True,host=ip,port=5000,threaded=True)
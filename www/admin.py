from flask import render_template,session,redirect,url_for,request,session,Blueprint
from www import db, bcrypt

abv = Blueprint('admin',__name__,template_folder='templates/admin')

class Admin():
    @abv.route('/')    
    def index():
        # return f'''{status}'''
        return render_template('index.html')

    @abv.route('/login',methods=['POST'])
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
    @abv.route('/admin')
    def admin():
        if 'userType' in session:
            if session['userType']==1:
                return render_template('admin.html')
            else:
                return redirect('/')
        else:
            return redirect('/')
    @abv.route('/logout')
    def logout():
        session.clear()
        return redirect('/')
    @abv.route('/users')
    def users():
        if 'userType' in session:
            if session['userType']==1:
                query = db.execute("SELECT * FROM tbl_user_accounts")
                data = query.fetchall()
                return render_template('user.html',data=data)
            else:
                return redirect('/')
        else:
            return redirect('/')
from flask import render_template,session,redirect,url_for,request,session,Blueprint,flash,escape
from www import db, bcrypt
import json

abv = Blueprint('admin',__name__,template_folder='templates/admin')

class Admin():
    @abv.route('/')
    def index():
        # return f'''{status}'''
        if 'userType' in session:
            if session['userType']==1:
                return redirect('/admin/dashboard')
            else:
                return redirect('/admin')
        else:
            return render_template('index.html')
    @abv.route('/province',methods=['POST'])
    def province():
        data = request.get_json(silent=True)
        reg = data['regCode']
        query = db.execute(f"SELECT * FROM refprovince WHERE regCode={reg}").fetchall()
        result = []
        for i in range(len(query)):
            result.append(dict(query[i]))
        return f'''{json.dumps(result)}'''
    @abv.route('/municipality',methods=['POST'])
    def municipality():
        data = request.get_json(silent=True)
        prov = data['provCode']
        query = db.execute(f"SELECT * FROM refcitymun WHERE provCode={prov}").fetchall()
        result = []
        for i in range(len(query)):
            result.append(dict(query[i]))
        return f'''{json.dumps(result)}'''
    @abv.route('/barangay',methods=['POST'])
    def barangay():
        data = request.get_json(silent=True)
        brgy = data['citymunCode']
        query = db.execute(f"SELECT * FROM refbrgy WHERE citymunCode={brgy}").fetchall()
        result = []
        for i in range(len(query)):
            result.append(dict(query[i]))
        return f'''{json.dumps(result)}'''
    @abv.route('/addSA',methods=['POST'])
    def addSA():
        fn = escape(request.form['fname'])
        ln = escape(request.form['lname'])
        mn = escape(request.form['mname'])
        br = escape(request.form['brgyCode'])
        bd = escape(request.form['dob'])
        dhr = escape(request.form['dh'])
        result = db.execute(f"SELECT st_fname,st_lname,st_mi FROM tbl_staff WHERE st_fname='{fn}' AND st_lname='{ln}' AND st_mi='{mn}'").fetchone()
        if result:
            flash(u"Already Registered",'warning')
        else:
            query = db.execute(f"INSERT INTO tbl_staff (st_fname, st_lname, st_mi, bday, date_hired, brgyCode) VALUES ('{fn}','{ln}','{mn}','{bd}','{dhr}','{br}')")
            db.commit()
            flash(u"Successfully Registered!",'success')
        # flash(u"Failed to Register!",'error')
        return redirect('/admin/addStaff')
    @abv.route('/delSA',methods=['POST'])
    def delSA():
        data = request.get_json(silent=True)
        ids = data['delData']
        for i in ids:
            query = db.execute(f"DELETE FROM tbl_staff WHERE staff_id={i}")
            db.commit()
        flash("Successfully Deleted!")    
        datas = {'status':'ok'}
        return f'''{json.dumps(dict(datas))}'''
    @abv.route('/login',methods=['POST'])
    def admin_login():
        mail = escape(request.form['email'])
        passwd = escape(request.form['pass'])
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
                return redirect('/admin/dashboard')
            else:
                flash(u"Invalid Credentials!",'warning')
                return redirect('/admin')
        else:
            flash(u"User Not Found!",'error')
            return redirect('/admin')
    @abv.errorhandler(KeyError)
    def key_error(error):
        # abv.logger.error('Unhandled Exception: %s', (e))
        flash(u"Something went wrong, please try again!",'keyerror')
        return f'''<script>window.history.go(-1);</script>'''
    @abv.route('/addStaff')
    def addStaff():
        if 'userType' in session:
            if session['userType']==1:
                reg = db.execute("SELECT * FROM refregion").fetchall()
                return render_template('addStaff.html',reg=reg)
            else:
                    return redirect('/')
        else:
            return redirect('/')        
    @abv.route('/dashboard')
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
        return redirect('/admin')
    @abv.route('/users')
    def users():
        if 'userType' in session:
            if session['userType']==1:
                data = db.execute("SELECT * FROm tbl_user_accounts").fetchall()
                return render_template('user.html',data=data)
            else:
                return redirect('/')
        else:
            return redirect('/')
    @abv.route('/staff')
    def staff():
        if 'userType' in session:
            if session['userType']==1:
                data = db.execute('''SELECT 
                    tbl_staff.staff_id,
                    tbl_staff.st_fname,
                    tbl_staff.st_lname,
                    tbl_staff.st_mi,
                    concat(refbrgy.brgyDesc," ",refcitymun.citymunDesc) as Address,
                    tbl_staff.bday,
                    tbl_staff.date_hired,
                    tbl_staff.date_created,
                    tbl_staff.brgyCode 
                    FROM tbl_staff inner join refbrgy 
                    ON refbrgy.brgyCode = tbl_staff.brgyCode 
                    LEFT JOIN refcitymun 
                    ON refcitymun.citymunCode=refbrgy.citymunCode;
                ''').fetchall()
                reg = db.execute("SELECT * FROM refregion").fetchall()
                return render_template('staff.html',data=data,reg=reg)
            else:
                return redirect('/')
        else:
            return redirect('/')

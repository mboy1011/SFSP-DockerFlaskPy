from flask import render_template,session,redirect,url_for,request,session,Blueprint
from www import db, bcrypt

ubv = Blueprint('user',__name__,template_folder='templates')

@ubv.route('/userpage')    
def index():
    # return f'''{status}'''
    return f'''User Page'''
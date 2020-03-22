from flask import render_template,session,redirect,url_for,request,session,Blueprint
from www import db, bcrypt

abv = Blueprint('admin',__name__,template_folder='templates')

@abv.route('/abvadmin')    
def index():
    # return f'''{status}'''
    return f'''Admin Page'''
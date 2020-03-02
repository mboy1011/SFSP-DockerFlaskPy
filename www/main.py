from flask import Flask
from view import View
import platform
import netifaces as ni

app = Flask(__name__)

ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] # Linux 

# Views
app.add_url_rule('/','index',View.index) # Main Page
if __name__ == "__main__":
    # Flask
    FLASK_APP="main"
    Flask.run(app,debug=True,host=ip,port=5000,threaded=True)
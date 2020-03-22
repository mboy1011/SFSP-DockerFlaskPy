from www import app,ip
if __name__ == "__main__":
    app.run(debug=True,host=ip,port=5000,threaded=True)
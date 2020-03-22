from www import app,ip
if __name__ == "__main__":
    # View()
    # Flask
    # FLASK_APP="main"
    app.run(debug=True,host=ip,port=5000,threaded=True)
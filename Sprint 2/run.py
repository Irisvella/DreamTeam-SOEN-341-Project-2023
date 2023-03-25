from app import create_app


app = create_app()  #starts the webserver and runs the app


if __name__=='__main__': 
    app.run(debug=True) #reruns the server automatically when python code is modified.
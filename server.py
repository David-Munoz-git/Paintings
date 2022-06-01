from flask_app import app
#import all controllers!
from flask_app.controllers import user_controller , painting_controller






if __name__=="__main__":
    app.run(debug=True)
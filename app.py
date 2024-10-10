from flask import Flask,Blueprint
from Routes.routes_accidents import accidents_bp
from Routes.routs_injuries import injuries_bp
app = Flask(__name__)

app.register_blueprint(accidents_bp)
app.register_blueprint(injuries_bp)
if __name__ == '__main__':
    app.run(debug=True)


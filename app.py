from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os


def get_app():
    app = Flask(__name__)
    CORS(app)

    # this part avoid chinese character encoding problem
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MINETYPE'] = 'application/json;charset=utf-8'
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

    # setting up sqlalchemy
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.db')
    return app

app = get_app()
api = Api(app)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return '<h1>The API is running<h1>'

if __name__ == '__main__':
    app.run(debug=True)



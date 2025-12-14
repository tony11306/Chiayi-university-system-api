from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging

from container import Container
from NcyuControllers.personal_course_controller import CourseEndpoint
from NcyuControllers.login_controller import LoginEndpoint
from NcyuControllers.grade_controller import GradeController
from NcyuControllers.course_selection_controller import CourseSelectionController

app = Flask(__name__)
CORS(app)
api = Api(app)

container = Container()
container.wire()

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MINETYPE'] = 'application/json;charset=utf-8'
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

api.add_resource(CourseEndpoint, '/course')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(GradeController, '/grade')
api.add_resource(CourseSelectionController, '/course_selection')

@app.route('/')
def index():
    return '<h1>The API is running<h1>'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=False)



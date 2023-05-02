from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
api = Api(app)

from SchoolSystemModel.personal_course import CourseEndpoint
from SchoolSystemModel.login import LoginEndpoint
from SchoolSystemModel.grades import GradeEndpoint
from SchoolSystemModel.course_selection import CourseSelectionEndpoint

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MINETYPE'] = 'application/json;charset=utf-8'
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

api.add_resource(CourseEndpoint, '/course')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(GradeEndpoint, '/grade')
api.add_resource(CourseSelectionEndpoint, '/course_selection')

@app.route('/')
def index():
    return '<h1>The API is running<h1>'

if __name__ == '__main__':
    app.run(debug=False)



from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from Model.db import db
import os



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

api = Api(app)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>The API is running<h1>'


from Handler.course_selection import CourseSelectionHandler
from Handler.login import LoginHandler
from Handler.personal_course import PersonalCourseHandler
from Handler.personal_grade import PersonalGradeHandler

from Service.course_service import CourseService
from Service.ncyu_proxy_service import NCYUProxyService

course_service = CourseService(db)
ncyu_proxy_service = NCYUProxyService()

api.add_resource(CourseSelectionHandler, '/course_selection', resource_class_kwargs={'course_service': course_service})
api.add_resource(LoginHandler, '/login', resource_class_kwargs={'ncyu_proxy_service': ncyu_proxy_service})
api.add_resource(PersonalCourseHandler, '/course', resource_class_kwargs={'ncyu_proxy_service': ncyu_proxy_service})
api.add_resource(PersonalGradeHandler, '/grade', resource_class_kwargs={'ncyu_proxy_service': ncyu_proxy_service})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)



from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from SchoolSystemModel.course import CourseEndpoint
from SchoolSystemModel.login import LoginEndpoint
from SchoolSystemModel.grades import GradeEndpoint

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MINETYPE'] = 'application/json;charset=utf-8'
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

api.add_resource(CourseEndpoint, '/course/<string:webpid1>')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(GradeEndpoint, '/grade/<string:webpid1>')

if __name__ == '__main__':
    app.run(debug=False)


